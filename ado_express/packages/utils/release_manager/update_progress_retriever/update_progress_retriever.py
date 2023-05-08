import base64
import logging

import requests

from ado_express.packages.authentication.ms_authentication.ms_authentication import \
    MSAuthentication
from ado_express.packages.common.enums.environment_statuses import \
    ReleaseEnvironmentStatuses
from ado_express.packages.common.environment_variables import \
    EnvironmentVariables
from ado_express.packages.common.models.deployment_status import \
    DeploymentStatus
from ado_express.packages.utils.asset_retrievers.release_environment_finder.release_environment_finder import \
    ReleaseEnvironmentFinder


class UpdateProgressRetriever:

    def __init__(self, ms_authentication: MSAuthentication, environment_variables: EnvironmentVariables):
        self.environment_variables = environment_variables
        self.release_client = ms_authentication.client
        self.environment_finder = ReleaseEnvironmentFinder(ms_authentication, environment_variables)

    def calculate_deployment_completion_percentage(self, deployment_tasks, latest_environment_deployment_status):
        completed_tasks = 0
        tasks = deployment_tasks['value']

        if tasks:
            total_tasks = deployment_tasks['count']
            for task in tasks:
                if str(task['status']).lower() in ['succeeded', 'partiallysucceeded', 'failed', 'canceled']: completed_tasks += 1

        percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        return percentage, completed_tasks, total_tasks
    
    def get_release_environment_tasks(self, release_project, release_id, environment_id, timeline_id, release_definition_id):
        generic_release_info = self.release_client.get_releases(project=release_project, definition_id=release_definition_id, release_id_filter=[release_id])
        
        for key, items in generic_release_info.__dict__.items():
            for item in items:
                release_base_url = item.url
            
                # Making direct API call because azure-devops doesn't provide a method to get tasks
                if (release_base_url):
                    api_url = f"{release_base_url}/environments/{environment_id}/attempts/1/timelines/{timeline_id}/tasks"
                    headers = {
                        'Authorization': f'Basic {str(base64.b64encode((f":{self.environment_variables.PERSONAL_ACCESS_TOKEN}").encode("ascii")).strip(), "ascii")}',
                        'Content-Type': 'application/json'
                    }
                    
                    response = requests.get(api_url, headers=headers)

                    if response.status_code == 200:
                        deployment_tasks = response.json()
                        return deployment_tasks
                    else:
                        raise Exception(f"Unable to get live deployment results for release: {release_id}.")

    def get_latest_deploy_step_from_environment_details(self, release_environment_modifications):
        deploy_steps = release_environment_modifications.deploy_steps
        sorted_deploy_steps = sorted(deploy_steps, key=lambda x: getattr(x, 'attempt'))
        latest_deploy_steps = sorted_deploy_steps[-1]

        return latest_deploy_steps
    
    def monitor_release_progress(self, release_project, updating_release, environment_id):
        release_id = updating_release.id
        release_definition_id = updating_release.release_definition.id
        all_tasks_completed = False
        latest_environment_deployment_status = None

        deploy_steps = self.get_environment_deploy_steps(release_project, release_id, environment_id)
        latest_environment_deployment_status = deploy_steps.status

        if latest_environment_deployment_status != ReleaseEnvironmentStatuses.InProgress.IN_PROGRESS.value:
            if latest_environment_deployment_status in ReleaseEnvironmentStatuses.Failed:
                return self.return_deployment_status("Something went wrong with the deployment, please check the errors on ADO.", 0, latest_environment_deployment_status)
            elif latest_environment_deployment_status in ReleaseEnvironmentStatuses.Succeeded:
                return self.return_deployment_status("The deployment process has finished successfully.", 100, latest_environment_deployment_status)
            else:
                return self.return_deployment_status("Waiting for deployment to start.", 0, latest_environment_deployment_status)
                    
        try:
            timeline_id_equivalent = deploy_steps.release_deploy_phases[0].run_plan_id
        except Exception as e:
            logging.error(f"Error: Failed to get timeline ID equivalent for release {release_id}, environment {environment_id}. Exception: {e}")
            return self.return_deployment_status("Live deployment data retrieval failed. Please check ADO and proceed manually.", 0, latest_environment_deployment_status)

        while not all_tasks_completed:
            try:
                release_tasks = self.get_release_environment_tasks(release_project, release_id, environment_id, timeline_id_equivalent, release_definition_id)

                if release_tasks:
                    percentage, completed_tasks, total_tasks = self.calculate_deployment_completion_percentage(release_tasks, latest_environment_deployment_status)

                    if percentage == 100:
                        all_tasks_completed = True
                        return self.return_deployment_status("All deployment tasks have been completed successfully, pending final confirmation call from release.", 100, latest_environment_deployment_status)
                    else:
                        return self.return_deployment_status(f"{completed_tasks}/{total_tasks} deployment tasks completed.", percentage, latest_environment_deployment_status)
                else:
                    return self.return_deployment_status("Unable to retrieve live deployment data. Deployment is still in progress.", 0, latest_environment_deployment_status)
            except Exception as e:
                logging.error(f"Error: Failed to get release environment tasks for release {release_id}, environment {environment_id}. Exception: {e}")
                return self.return_deployment_status("Live deployment data retrieval failed. Please check ADO and proceed manually.", 0, latest_environment_deployment_status)

    def get_environment_deploy_steps(self, release_project, release_id, environment_id):
        release_environment = self.environment_finder.get_release_environment_by_id(release_project, release_id, environment_id)
        deploy_steps = self.get_latest_deploy_step_from_environment_details(release_environment)
        return deploy_steps
    
    def return_deployment_status(self, comment, percentage, status):
        live_deployment_status = DeploymentStatus(comment,percentage,status)
        return live_deployment_status
            
