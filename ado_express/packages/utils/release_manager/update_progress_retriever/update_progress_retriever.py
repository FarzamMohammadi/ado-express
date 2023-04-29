import base64
import time

import requests

from ado_express.packages.authentication.ms_authentication.ms_authentication import \
    MSAuthentication
from ado_express.packages.common.enums.environment_statuses import \
    ReleaseEnvironmentStatuses
from ado_express.packages.common.environment_variables import \
    EnvironmentVariables
from ado_express.packages.utils.asset_retrievers.release_environment_finder.release_environment_finder import \
    ReleaseEnvironmentFinder


class UpdateProgressRetriever:

    def __init__(self, ms_authentication: MSAuthentication, environment_variables: EnvironmentVariables):
        self.environment_variables = environment_variables
        self.release_client = ms_authentication.client
        self.environment_finder = ReleaseEnvironmentFinder(ms_authentication, environment_variables)

    def calculate_deployment_completion_percentage(self, deployment_tasks):
        completed_tasks = 0
        tasks = deployment_tasks['value']

        if tasks:
            total_tasks = deployment_tasks['count']
            for task in tasks:
                print(task)
                print(task['status'])
                if str(task['status']).lower() in ['succeeded', 'partiallysucceeded', 'failed', 'canceled']: completed_tasks += 1

        percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        return percentage
    
    def get_release_environment_tasks(self, release_project, release_id, environment_id, timeline_id):
        generic_release_info = self.release_client.get_releases(project=release_project, definition_id=90, release_id_filter=[release_id])

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
        release_definition = updating_release.release_definition
        release_id = updating_release.id
        all_tasks_completed = False
        latest_environment_deployment_status = None
        seconds_to_sleep_between_calls = 2
        
        # TODO Check that it has not succeeded (and maybe other statuses we dont want to get stuck in)
        while latest_environment_deployment_status != ReleaseEnvironmentStatuses.InProgress.IN_PROGRESS.value:
            deploy_steps = self.get_environment_deploy_steps(release_project, release_id, environment_id)
            latest_environment_deployment_status = deploy_steps.status

            if latest_environment_deployment_status != ReleaseEnvironmentStatuses.InProgress.IN_PROGRESS.value: 
                print(f"Release: {release_definition.name}, Deployment Status: {latest_environment_deployment_status}")
                time.sleep(seconds_to_sleep_between_calls)

            
        #TODO add trycatch for empty array
        timeline_id_equivalent = deploy_steps.release_deploy_phases[0].run_plan_id
        
        while not all_tasks_completed:
            release_tasks = self.get_release_environment_tasks(release_project, release_id, environment_id, timeline_id_equivalent)

            if release_tasks:
                percentage = self.calculate_deployment_completion_percentage(release_tasks)
                print(f"Release: {release_definition.name}, Progress: {percentage:.2f}%")
                
                if percentage == 100:
                    all_tasks_completed = True 
                elif percentage < 100:
                    time.sleep(seconds_to_sleep_between_calls)
            else:
                print("Error fetching release status.")
                all_tasks_completed = True 

        while latest_environment_deployment_status != ReleaseEnvironmentStatuses.Succeeded.SUCCEEDED.value:
            time.sleep(seconds_to_sleep_between_calls)
            latest_environment_deployment_status = self.get_environment_deploy_steps(release_project, release_id, environment_id).status
        
        print(f"Release: {release_definition.name}, Final Deployment Status: {latest_environment_deployment_status}")
        return latest_environment_deployment_status
    
    def get_environment_deploy_steps(self, release_project, release_id, environment_id):
        release_environment = self.environment_finder.get_release_environment_by_id(release_project, release_id, environment_id)
        deploy_steps = self.get_latest_deploy_step_from_environment_details(release_environment)
        return deploy_steps
            
