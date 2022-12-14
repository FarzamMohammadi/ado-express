import concurrent.futures
from itertools import repeat
import logging
import os
import sys
import time
from datetime import datetime

from packages.authentication import MSAuthentication
from packages.common.constants import Constants
from packages.common.environment_variables import EnvironmentVariables
from packages.common.models import DeploymentDetails
from packages.utils import DeploymentPlan
from packages.utils.asset_retrievers.release_finder import ReleaseFinder
from packages.utils.asset_retrievers.work_item_manager.work_item_manager import WorkItemManager
from packages.utils.excel_manager import ExcelManager
from packages.utils.release_manager.update_release import UpdateRelease
from packages.utils.release_note_helpers import needs_deployment
from pytz import timezone

logging.basicConfig(filename=Constants.LOG_FILE_PATH, encoding='utf-8', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')
logging.info('Starting application')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

constants = Constants()
deployment_plan_file_headers = constants.DEPLOYMENT_PLAN_HEADERS
deployment_plan_path = constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH
environment_variables = EnvironmentVariables()
deployment_plan = DeploymentPlan(constants, environment_variables)
excel_manager = ExcelManager()

class Startup:

    def __init__(self):
        self.load_dependencies()
        self.initialize_logging()
    
    def initialize_logging(self):
        if self.search_only:
            logging.info('Starting the search...')

            if os.path.isfile(self.search_file_path):
                with open(self.search_file_path, "a") as file:
                    file.write(f"\n\nNew Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n")
            else:
                with open(self.search_file_path, "a") as file:
                    file.write(f"New Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n")
        else:
            logging.info('Starting the update...')
        
    def initialize_excel_configurations(self):
            # Create new deployment excel file
            new_df = excel_manager.create_dataframe(deployment_plan_file_headers)
            excel_manager.save_or_concat_file(new_df, deployment_plan_path, True) 
        
    def load_dependencies(self):
        self.ms_authentication = MSAuthentication(environment_variables)
        self.release_finder = ReleaseFinder(self.ms_authentication, environment_variables)
        self.search_only = environment_variables.SEARCH_ONLY
        self.search_file_path = constants.SEARCH_RESULTS_FILE_PATH
        self.via_env = environment_variables.VIA_ENV
        self.query = environment_variables.QUERY
        self.time_format = '%Y-%m-%d %H:%M:%S'
        self.datetime_now = datetime.now(timezone('US/Eastern'))

    def get_crucial_release_definitions(self):
        crucial_release_definitions = []
        # First checks command line args, if not found, then checks the deployment plan
        if environment_variables.CRUCIAL_RELEASE_DEFINITIONS is not None:
            crucial_release_definitions = environment_variables.CRUCIAL_RELEASE_DEFINITIONS
        else:
            for deployment_detail in deployment_plan_details:
                if deployment_detail.is_crucial:
                    crucial_release_definitions.append(deployment_detail.release_name)
        
        return crucial_release_definitions

    def get_deployment_details_from_query(self):
        work_item_manager = WorkItemManager(self.ms_authentication)
        build_ids = work_item_manager.get_query_build_ids(self.query)
        releases_dict = self.release_finder.get_releases_via_builds(build_ids)
        rollback_dict = dict()
        deployment_details = []

        if not releases_dict: return deployment_details # If no releases are found

        # Get rollback
        with concurrent.futures.ThreadPoolExecutor() as executor:
            rollbacks = executor.map(self.release_finder.get_release, {k for k, v in releases_dict.items()}, repeat(self.via_env), repeat(True))

            for rollback in rollbacks:
                if all(rollback.values()): rollback_dict |= rollback # If rollback for target environment is found
                else: releases_dict.pop(next(iter(rollback))) # Remove key & value from releases_dict

        for release_location, target_release in releases_dict.items():
            project = release_location.split('/')[0] 
            release_name = release_location.split('/')[1]
            rollback_release = rollback_dict[release_location]
            target_release_number = target_release.split('-')[1]
            rollback_release_number = rollback_release.split('-')[1]

            if (needs_deployment(target_release_number, rollback_release_number)):
                deployment_detail = DeploymentDetails(project, release_name, target_release_number, rollback_release_number)
                deployment_details.append(deployment_detail)

            logging.info(f'Release found from query: Project:{project}, Release Definition:{release_name}, Target:{target_release_number}, Rollback:{rollback_release_number}')
        
        return deployment_details

    def get_deployment_detail_from_latest_release(self, deployment_detail: DeploymentDetails):
        try:
            target_release = self.release_finder.get_release(deployment_detail, find_via_env=self.via_env)
            rollback_release = self.release_finder.get_release(deployment_detail, find_via_env=self.via_env, rollback=True)
            target_release_number = target_release.name.split('-')[1]
            rollback_release_number = rollback_release.name.split('-')[1]

            if (needs_deployment(target_release_number, rollback_release_number)): 
                deployment_detail = DeploymentDetails(deployment_detail.release_project_name, deployment_detail.release_name, target_release_number, rollback_release_number, deployment_detail.is_crucial)
                
                logging.info(f'Latest release found: Project:{deployment_detail.release_project_name}, Release Definition:{deployment_detail.release_name}, Target:{target_release_number}, Rollback:{rollback_release_number}')
                return deployment_detail
        except:
            logging.error(f'Latest release not found: Project:{deployment_detail.release_project_name}, Release Definition:{deployment_detail.release_name}\n - Possible cause: The release does not have either the source or target stage you are looking for')
            return
    
    def search_and_log_details_only(self, deployment_detail: DeploymentDetails):
        self.release_finder.get_releases(deployment_detail, find_via_env=self.via_env)
    
    def deploy(self, deployment_detail: DeploymentDetails):
        try:
            if deployment_detail is not None: # The ThreadPoolExecutor may return None for some releases
                release_to_update = self.release_finder.get_release(deployment_detail, find_via_env=self.via_env)
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
    startup = Startup()
    task_start = time.perf_counter() 
    deployment_details = None

    # If a query is provided then do query run first (it'll either be deployed later or stop after notes creation)
    if environment_variables.QUERY:
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
        if environment_variables.QUERY or environment_variables.VIA_ENV_LATEST_RELEASE:
            if deployment_details:
                logging.info(f'Exporting Release notes to: {constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH}')
                startup.initialize_excel_configurations()

                for deployment_detail in deployment_details:
                    if deployment_detail is not None: # The ThreadPoolExecutor may return None for some releases

                        row = excel_manager.convert_deplyoment_detail_to_excel_row(deployment_plan_file_headers, deployment_detail)
                        excel_manager.save_or_concat_file(row, deployment_plan_path)
            else: logging.info(f'No results found - please check the configuration')
        else:    
            # Else run a log-only search
            for deployment_detail in deployment_plan_details:
                startup.search_and_log_details_only(deployment_detail)

    # Run deployment
    else:
        crucial_release_definitions = startup.get_crucial_release_definitions()
        crucial_deployment_details = []

        # Set deployment details to deployment plan details if it's not a query/latest release run
        deployment_details = deployment_plan_details if deployment_details is None else deployment_details
        
        if deployment_details is None:
            logging.error(f'No deployment details found - please check the configuration')
            exit()
        else:
            if crucial_release_definitions:
                # Separate crucial & regular deployments based on release defintions that match CRUCIAL_RELEASE_DEFINITIONS env variable list
                crucial_deployment_details = [x for x in deployment_details if x.release_name in crucial_release_definitions]
                deployment_details[:] = [x for x in deployment_details if x.release_name not in crucial_release_definitions]

            if crucial_deployment_details: # First, deploy crucial releases if there are any
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    logging.info('Deploying the crucial releases first')
                    executor.map(startup.deploy, crucial_deployment_details)
                    executor.shutdown(wait=True)

            with concurrent.futures.ThreadPoolExecutor() as executor: # Then, deploy the rest of the releases
                if crucial_deployment_details: 
                    logging.info('Deploing the rest of the releases')
                else:
                    logging.info('Deploying releases')
                executor.map(startup.deploy, deployment_details)

    task_end = time.perf_counter()
    logging.info(f'Tasks completed in {task_end-task_start} seconds')