import os
import sys

# Needed to enable segregation of projects
sys.path.append(os.path.abspath("."))

import concurrent.futures
from itertools import repeat
import logging
import sys
import time
from datetime import datetime

from ado_express.packages.authentication import MSAuthentication
from ado_express.packages.common.constants import Constants
from ado_express.packages.common.enums.explicit_release_types import ExplicitReleaseTypes
from ado_express.packages.common.environment_variables import EnvironmentVariables
from ado_express.packages.common.models import DeploymentDetails
from ado_express.packages.utils import DeploymentPlan
from ado_express.packages.utils.asset_retrievers.release_finder import ReleaseFinder
from ado_express.packages.utils.asset_retrievers.work_item_manager.work_item_manager import WorkItemManager
from ado_express.packages.utils.excel_manager import ExcelManager
from ado_express.packages.utils.release_manager.update_release import UpdateRelease
from ado_express.packages.utils.release_note_helpers import needs_deployment
from pytz import timezone

logging.basicConfig(filename=Constants.LOG_FILE_PATH, encoding='utf-8', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')
logging.info('Starting application')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

constants = Constants()
deployment_plan_file_headers = constants.DEPLOYMENT_PLAN_HEADERS
deployment_plan_path = constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH
excel_manager = ExcelManager()

class Startup:

    def __init__(self, environment_variables):
        self.environment_variables = environment_variables
        self.load_dependencies()
        self.initialize_logging()
    
    #TODO: Create logger class & include this
    def initialize_logging(self):
        if self.search_only:
            logging.info('Starting the search...')
            logging.info(f"Search Date & Time:{self.datetime_now.strftime(self.time_format)}\nResults:\n")
        else:
            logging.info('Starting the update...')
        
    def initialize_excel_configurations(self):
            # Create new deployment excel file
            new_df = excel_manager.create_dataframe(deployment_plan_file_headers)
            excel_manager.save_or_concat_file(new_df, deployment_plan_path, True) 


    def updated_deployment_details_based_on_explicit_inclusion_and_exclusion(self, deployment_details):
        new_deployment_details = []
        explicit_deployment_values = environment_variables.EXPLICIT_RELEASE_VALUES

        if explicit_deployment_values is None: return deployment_details

        releases_to_deploy = explicit_deployment_values.get(ExplicitReleaseTypes.INCLUDE)
        releases_not_to_deploy = explicit_deployment_values.get(ExplicitReleaseTypes.EXCLUDE)

        if releases_to_deploy: [new_deployment_details.append(deployment_detail) if deployment_detail.release_name in releases_to_deploy else 99999 for deployment_detail in deployment_details]
        elif releases_not_to_deploy: [new_deployment_details.append(deployment_detail) if deployment_detail.release_name not in releases_not_to_deploy else 99999 for deployment_detail in deployment_details]

        if new_deployment_details == []: logging.error('Found no releases based on the explicit release values provided.')

        return new_deployment_details

    def load_dependencies(self):
        self.ms_authentication = MSAuthentication(self.environment_variables)
        self.release_finder = ReleaseFinder(self.ms_authentication, self.environment_variables)
        self.search_only = self.environment_variables.SEARCH_ONLY
        self.via_env = self.environment_variables.VIA_ENV
        self.via_latest = self.environment_variables.VIA_ENV_LATEST_RELEASE
        self.queries = self.environment_variables.QUERIES
        self.time_format = '%Y-%m-%d %H:%M:%S'
        self.datetime_now = datetime.now(timezone('US/Eastern'))

    def get_crucial_release_definitions(self, deployment_details):
        crucial_release_definitions = []
        # First checks command line args, if not found, then checks the deployment plan file
        if environment_variables.CRUCIAL_RELEASE_DEFINITIONS is not None:
            crucial_release_definitions = environment_variables.CRUCIAL_RELEASE_DEFINITIONS
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

        if not found_releases: return deployment_details # If no releases are found

        # Get rollback
        with concurrent.futures.ThreadPoolExecutor() as executor:
            rollbacks = executor.map(self.release_finder.get_release, {k for k, v in found_releases.items()}, repeat(self.via_env), repeat(True), repeat(self.via_latest))

            for rollback in rollbacks:
                if all(rollback.values()): rollback_dict |= rollback # If rollback for target environment is found
                else: found_releases.pop(next(iter(rollback))) # Remove key & value from found_releases

        for release_location, target_release in found_releases.items():
            project = release_location.split('/')[0] 
            release_name = release_location.split('/')[1]
            rollback_release = rollback_dict[release_location]
            target_release_number = target_release.split('-')[1]
            rollback_release_number = rollback_release.split('-')[1]

            if needs_deployment(target_release_number, rollback_release_number):
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

            if needs_deployment(target_release_number, rollback_release_number):
                deployment_detail = DeploymentDetails(deployment_detail.release_project_name, deployment_detail.release_name, target_release_number, rollback_release_number, deployment_detail.is_crucial)
                
                logging.info(f'Latest release found: Project:{deployment_detail.release_project_name}, Release Definition:{deployment_detail.release_name}, Target:{target_release_number}, Rollback:{rollback_release_number}')
                return deployment_detail
            else: return None
        except:
            logging.error(f'Latest release not found: Project:{deployment_detail.release_project_name}, Release Definition:{deployment_detail.release_name}\n - Possible cause: The release does not have either the source or target stage you are looking for')
            return None
    
    def search_and_log_details_only(self, deployment_detail: DeploymentDetails):
        return self.release_finder.get_releases(deployment_detail, find_via_env=self.via_env)
    
    def deploy(self, deployment_detail: DeploymentDetails):
        try:
            if deployment_detail is not None: # The ThreadPoolExecutor may return None for some releases
                release_to_update = self.release_finder.get_release(deployment_detail, self.via_env, False, self.via_latest)
                update_manager = UpdateRelease(constants, self.ms_authentication, environment_variables, self.release_finder)

                update_attempt = update_manager.update_release(deployment_detail, release_to_update)
                update_attempt_successful = update_attempt[0]
                update_comment = update_attempt[1]

                if update_attempt_successful:
                    # Check the status of release update
                    logging.info(f'Monitoring update Status - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{environment_variables.RELEASE_TARGET_ENV}')
                    release_updated_successfully = update_manager.get_release_update_result(deployment_detail, release_to_update)

                    if not release_updated_successfully:
                        update_manager.handle_failed_update(deployment_detail, self.via_env)
                    else:
                        logging.info(f'Release Update Successful - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{environment_variables.RELEASE_TARGET_ENV}')
                else:
                    update_manager.handle_failed_update(deployment_detail, self.via_env, failure_reason=update_comment)

        except Exception as e:
            logging.error(f'There was an error. Please check their status and continue manually.\nException:{e}')

if __name__ == '__main__':
    environment_variables = EnvironmentVariables()
    deployment_plan = DeploymentPlan(constants, environment_variables)
    startup = Startup(environment_variables)
    task_start = time.perf_counter() 
    deployment_details = None

    # If a query is provided then do query run first (it'll either be deployed later or stop after notes creation)
    if environment_variables.QUERIES:
        deployment_details = startup.get_deployment_details_from_query()
    else:
        # If not a query run then get deployment details from deployment plan
        deployment_plan_details = deployment_plan.get_data_from_deployment_plan_file()
        # Use deployment plan to get deployment details
        if environment_variables.VIA_ENV_LATEST_RELEASE:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                    deployment_details = executor.map(startup.get_deployment_detail_from_latest_release, deployment_plan_details)
    # Run search 
    if environment_variables.SEARCH_ONLY:
        # If doing a release notes search then create and export deployment details to excel file
        if environment_variables.QUERIES or environment_variables.VIA_ENV_LATEST_RELEASE:
            if deployment_details:
                logging.info(f'Exporting Release notes to: {constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH}')
                startup.initialize_excel_configurations()

                for deployment_detail in deployment_details:
                    if deployment_detail is not None: # The ThreadPoolExecutor may return None for some releases

                        row = excel_manager.convert_deployment_detail_to_excel_row(deployment_plan_file_headers, deployment_detail)
                        excel_manager.save_or_concat_file(row, deployment_plan_path)
            else: logging.info(f'No results found - please check the configuration')
        else:    
            # Else run a log-only search
            for deployment_detail in deployment_plan_details:
                startup.search_and_log_details_only(deployment_detail)

    # Run deployment
    else:
        # Set deployment details to deployment plan details if it's not a query/latest release run
        deployment_details = deployment_plan_details if deployment_details is None else deployment_details

        deployment_details = startup.updated_deployment_details_based_on_explicit_inclusion_and_exclusion(deployment_details)
        
        #TODO: Create logger class & include this
        if deployment_details is None:
            logging.error(f'No deployment details found - please check the configurations')
            logging.error(f'Stopping process :(')
            exit()

        crucial_release_definitions = startup.get_crucial_release_definitions(deployment_details)
        crucial_deployment_details = []

        if crucial_release_definitions:
            # Separate crucial & regular deployments based on release definitions that match CRUCIAL_RELEASE_DEFINITIONS env variable list
            crucial_deployment_details = [x for x in deployment_details if x.release_name in crucial_release_definitions]
            deployment_details[:] = [x for x in deployment_details if x.release_name not in crucial_release_definitions]

        if crucial_deployment_details: # First, deploy crucial releases if there are any
            with concurrent.futures.ThreadPoolExecutor() as executor:
                logging.info('Deploying the crucial releases first')
                
                executor.map(startup.deploy, crucial_deployment_details)
                executor.shutdown(wait=True)

        with concurrent.futures.ThreadPoolExecutor() as executor: # Then, deploy the rest of the releases
            if crucial_deployment_details: 
                logging.info('Deploying the rest of the releases')
            else:
                logging.info('Deploying releases')
            
            executor.map(startup.deploy, deployment_details)

    task_end = time.perf_counter()
    logging.info(f'Tasks completed in {task_end-task_start} seconds')