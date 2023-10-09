import concurrent.futures
import logging
from itertools import repeat

from ado_express.packages.authentication import MSAuthentication
from ado_express.packages.shared import Constants, EnvironmentVariables
from ado_express.packages.shared.enums import DeploymentStatusLabel, ExplicitReleaseTypes
from ado_express.packages.shared.models import DeploymentDetails, DeploymentStatus
from ado_express.packages.toolbox import (ExcelManager, Logger,
                                          ReleaseEnvironmentFinder,
                                          ReleaseFinder,
                                          UpdateProgressRetriever,
                                          UpdateRelease, WorkItemManager,
                                          run_helpers)


class ADOExpress:

    def __init__(self, environment_variables: EnvironmentVariables):
        self.constants = Constants()
        self.excel_manager = ExcelManager()

        self.environment_variables = environment_variables
        self.load_dependencies()

        Logger(run_helpers.is_running_as_executable()).log_the_start_of_application(self.search_only)

    def load_dependencies(self):
        self.ms_authentication = MSAuthentication(self.environment_variables)
        self.release_finder = ReleaseFinder(self.ms_authentication, self.environment_variables)
        self.search_only = self.environment_variables.SEARCH_ONLY
        self.via_env = self.environment_variables.VIA_ENV
        self.via_latest = self.environment_variables.VIA_ENV_LATEST_RELEASE
        self.queries = self.environment_variables.QUERIES
    
    def prepare_result_excel_file(self):
        new_df = self.excel_manager.create_dataframe(self.constants.DEPLOYMENT_PLAN_HEADERS)
        self.excel_manager.save_or_concat_file(new_df, self.constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH, True) 

    def updated_deployment_details_based_on_explicit_inclusion_and_exclusion(self, deployment_details):
        new_deployment_details = []
        explicit_deployment_values = self.environment_variables.EXPLICIT_RELEASE_VALUES

        if explicit_deployment_values is None: return deployment_details

        releases_to_deploy = explicit_deployment_values.get(ExplicitReleaseTypes.INCLUDE)
        releases_not_to_deploy = explicit_deployment_values.get(ExplicitReleaseTypes.EXCLUDE)

        if releases_to_deploy: [new_deployment_details.append(deployment_detail) if deployment_detail.release_name in releases_to_deploy else 99999 for deployment_detail in deployment_details]
        elif releases_not_to_deploy: [new_deployment_details.append(deployment_detail) if deployment_detail.release_name not in releases_not_to_deploy else 99999 for deployment_detail in deployment_details]

        if new_deployment_details == []: logging.error('Found no releases based on the explicit release values provided.')

        return new_deployment_details

    def get_crucial_release_definitions(self, deployment_details):
        crucial_release_definitions = []
        # First checks command line args, if not found, then checks the deployment plan file
        if self.environment_variables.CRUCIAL_RELEASE_DEFINITIONS is not None and self.environment_variables.CRUCIAL_RELEASE_DEFINITIONS != []:
            crucial_release_definitions = self.environment_variables.CRUCIAL_RELEASE_DEFINITIONS
        else:
            for deployment_detail in deployment_details:
                if deployment_detail.is_crucial:
                    crucial_release_definitions.append(deployment_detail.release_name)
        
        return crucial_release_definitions

    def get_deployment_details_from_query(self):
        work_item_manager = WorkItemManager(self.ms_authentication)
        found_releases = dict()

        for query in self.queries:
            build_ids = work_item_manager.get_query_build_ids(query)
            search_result_releases = self.release_finder.get_releases_via_builds(build_ids)

            for release_definition in search_result_releases:
                if release_definition not in found_releases: found_releases[release_definition] = search_result_releases[release_definition]
                elif found_releases[release_definition] < search_result_releases[release_definition]: found_releases[release_definition] = search_result_releases[release_definition]

        rollback_dict = dict()
        deployment_details = []

        if not found_releases: return deployment_details

        # Get rollback
        with concurrent.futures.ThreadPoolExecutor() as executor:
            rollbacks = executor.map(self.release_finder.get_release, {k for k, v in found_releases.items()}, repeat(self.via_env), repeat(True), repeat(self.via_latest))

            for rollback in rollbacks:
                if all(rollback.values()): rollback_dict |= rollback # If found rollback, add it to rollback_dict
                else: found_releases.pop(next(iter(rollback))) # Else remove release key & value from found_releases

        for release_location, target_release in found_releases.items():
            project = release_location.split('/')[0] 
            release_name = release_location.split('/')[1]
            rollback_release = rollback_dict[release_location]
            target_release_number = target_release.split('-')[1]
            rollback_release_number = rollback_release.split('-')[1]

            if run_helpers.needs_deployment(target_release_number, rollback_release_number):
                deployment_detail = DeploymentDetails(project, release_name, target_release_number, rollback_release_number)
                deployment_details.append(deployment_detail)

                logging.info(f'Release found from query: Project:{project}, Release Definition:{release_name}, Target:{target_release_number}, Rollback:{rollback_release_number}')
        
        return deployment_details

    def get_deployment_detail_from_latest_release(self, deployment_detail: DeploymentDetails):
        try:
            target_release = self.release_finder.get_release(deployment_detail, find_via_env=self.via_env, rollback=False, via_latest=self.via_latest)
            rollback_release = self.release_finder.get_release(deployment_detail, find_via_env=self.via_env, rollback=True, via_latest=self.via_latest)
            target_release_number = target_release.name.split('-')[1]
            rollback_release_number = rollback_release.name.split('-')[1]

            if run_helpers.needs_deployment(target_release_number, rollback_release_number):
                deployment_detail = DeploymentDetails(deployment_detail.release_project_name, deployment_detail.release_name, target_release_number, rollback_release_number, deployment_detail.is_crucial)
                
                logging.info(f'Latest release found: Project:{deployment_detail.release_project_name}, Release Definition:{deployment_detail.release_name}, Target:{target_release_number}, Rollback:{rollback_release_number}')
                return deployment_detail
            else: return logging.info(f'No Deployable releases found: Project:{deployment_detail.release_project_name}, Release Definition:{deployment_detail.release_name}, Latest release found: Target:{target_release_number}, Rollback:{rollback_release_number}')

        except:
            logging.error(f'Latest release not found: Project:{deployment_detail.release_project_name}, Release Definition:{deployment_detail.release_name}\n - Possible cause: The release does not have either the source or target stage you are looking for')
            return None
    
    def search_and_log_details_only(self, deployment_detail: DeploymentDetails):
        return self.release_finder.get_releases(deployment_detail, find_via_env=self.via_env)
        
    def deploy_to_target_or_rollback(self, deployment_detail: DeploymentDetails, rollback: bool=False):
        try:
            if deployment_detail is not None: # The ThreadPoolExecutor may return None for some releases
                update_manager = UpdateRelease(self.constants, self.ms_authentication, self.environment_variables, self.release_finder)
                
                release_to_update = self.release_finder.get_release(deployment_detail, self.via_env, rollback, self.via_latest)

                if rollback: 
                    logging.info(f'Attempting to rollback: {deployment_detail.release_name}')
                    update_manager.roll_back_release(deployment_detail, release_to_update)

                    return True
                else:
                    update_manager = UpdateRelease(self.constants, self.ms_authentication, self.environment_variables, self.release_finder)
                    attempt_was_successful, update_error = update_manager.update_release(deployment_detail, release_to_update)

                    if not attempt_was_successful:
                        logging.error(f'There was an error with deployment for: {deployment_detail.release_name}.\n:{update_error}')

                return attempt_was_successful
        except Exception as e:
            logging.error(f'There was an error with deployment for: {deployment_detail.release_name}. Please check their status and continue manually.\nException:{e}')
            return False
        
    def get_deployment_status(self, deployment_detail: DeploymentDetails, rollback: bool=False):
        try:
            if deployment_detail is not None:
                try:
                    updating_release = self.release_finder.get_release(deployment_detail, self.via_env, rollback, self.via_latest)
                except IndexError:
                    errorMessage = f"Error: Cannot find the release for {deployment_detail.release_name}"
                    logging.error(errorMessage)
                    
                    deployment_status = DeploymentStatus(errorMessage, 0, DeploymentStatusLabel.failed)
                    return deployment_status

                try:
                    release_environment_finder = ReleaseEnvironmentFinder(self.ms_authentication, self.environment_variables)
                    updating_release_environment = release_environment_finder.get_release_environment(deployment_detail, updating_release.id)
                except IndexError:
                    errorMessage = f"Error: Cannot find the release environment for {deployment_detail.release_name} and release ID {updating_release.id}"
                    logging.error(errorMessage)
                    
                    deployment_status = DeploymentStatus(errorMessage, 0, DeploymentStatusLabel.failed)
                    return deployment_status

                release_progress = UpdateProgressRetriever(self.ms_authentication, self.environment_variables)
                current_deployment_status = release_progress.monitor_release_progress(deployment_detail.release_project_name, updating_release, updating_release_environment.id)

                return current_deployment_status

        except Exception as e:
            logging.error(f'There was an error with retrieving live deployment status of {updating_release.release_definition}.\nException:{e}')


    def release_deployment_completed(self, deployment_detail, rollback=False): 
        update_manager = UpdateRelease(self.constants, self.ms_authentication, self.environment_variables, self.release_finder)
        
        release_to_update = self.release_finder.get_release(deployment_detail, self.via_env, rollback, self.via_latest)
        
        deployment_is_complete, successfully_completed = update_manager.is_deployment_complete(deployment_detail, release_to_update)
        
        return deployment_is_complete, successfully_completed
    
    def run_release_deployments(self, deployment_details, is_deploying_crucial_releases, rollback=False, had_crucial_releases=False):
        releases = []
        
        if is_deploying_crucial_releases: logging.info('Deploying the crucial releases first')
        
        with concurrent.futures.ThreadPoolExecutor() as executor: # Then, deploy the rest of the releases
            if not is_deploying_crucial_releases and had_crucial_releases: 
                logging.info('Deploying the rest of the releases')
            elif not is_deploying_crucial_releases and had_crucial_releases:
                logging.info('Deploying releases')
            
            releases = executor.map(self.deploy_to_target_or_rollback, deployment_details, repeat(rollback))
        
        return releases
    
    def get_crucial_deployment_from_deployment_details(self, deployment_details, crucial_release_definitions):
        return [x for x in deployment_details if x.release_name in crucial_release_definitions]
    
    def remove_crucial_deployments_from_deployment_details(self, deployment_details, crucial_release_definitions):
        return [x for x in deployment_details if x.release_name not in crucial_release_definitions]