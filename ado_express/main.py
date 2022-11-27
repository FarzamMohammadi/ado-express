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

            if self.via_stage_latest_release or self.query:
                # Create new deployment excel file
                self.deployment_plan_columns = constants.DEPLOYMENT_PLAN_HEADERS
                self.deployment_plan_path = constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH
                new_df = excel_manager.create_dataframe(self.deployment_plan_columns)
                excel_manager.save_or_concat_file(new_df, constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH, True)
                
            if os.path.isfile(self.search_file_path):
                with open(self.search_file_path, "a") as file:
                    file.write(f"\n\nNew Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n")
            else:
                with open(self.search_file_path, "a") as file:
                    file.write(f"New Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n")
        else:
            logging.info('Starting the update...')
        
    def load_dependencies(self):
        self.ms_authentication = MSAuthentication(environment_variables)
        self.release_finder = ReleaseFinder(self.ms_authentication, deployment_plan.deployment_details, environment_variables)
        self.search_only = environment_variables.SEARCH_ONLY
        self.search_file_path = constants.SEARCH_RESULTS_FILE_PATH
        self.via_stage = environment_variables.VIA_STAGE
        self.via_stage_latest_release = environment_variables.VIA_STAGE_LATEST_RELEASE
        self.query = environment_variables.QUERY
        self.time_format = '%Y-%m-%d %H:%M:%S'
        self.datetime_now = datetime.now(timezone('US/Eastern'))
    
    def start_request(self, deployment_detail: DeploymentDetails):
        if self.search_only:
            try:
                if self.query is not None:
                    work_item_manager = WorkItemManager(self.ms_authentication)
                    build_ids = work_item_manager.get_query_build_ids(self.query)
                    releases_dict = self.release_finder.get_releases_via_builds(build_ids)
                    rollback_dict = dict()
                    rows = []

                    # Get rollback
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        rollbacks = executor.map(self.release_finder.get_release, {k for k, v in releases_dict.items()}, repeat(self.via_stage), repeat(True))

                        for rollback in rollbacks:
                            if all(rollback.values()): rollback_dict |= rollback # If rollback for target environment is found
                            else: releases_dict.pop(next(iter(rollback))) # Remove key & value from releases_dict

                    for release_location, release_target in releases_dict.items():
                        project = release_location.split('/')[0] 
                        release_name = release_location.split('/')[1]
                    
                        new_row = excel_manager.pd.DataFrame({
                            self.deployment_plan_columns[0]: project, 
                            self.deployment_plan_columns[1]: release_name, 
                            self.deployment_plan_columns[2]: release_target, 
                            self.deployment_plan_columns[3]: rollback_dict[release_location],
                            self.deployment_plan_columns[4]: ''
                            }, index=[0])
                        
                        rows.append(new_row)
                    
                    return rows

                elif self.via_stage_latest_release:
                    target_release = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage)
                    rollback_release = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage, rollback=True)

                    if (needs_deployment(target_release, rollback_release)):
                        with open(self.search_file_path, "a") as file:
                            file.write(f"""
                            \n{deployment_detail.release_name} Results:
                            Target Release: {target_release.name} (Based on last release in '{environment_variables.VIA_STAGE_SOURCE_NAME}' stage)
                            Rollback Release: {rollback_release.name} (Based on last release in '{environment_variables.RELEASE_STAGE_NAME}' stage)
                            """)

                        new_row = excel_manager.pd.DataFrame({
                            self.deployment_plan_columns[0]: str(deployment_detail.release_project_name), 
                            self.deployment_plan_columns[1]: str(deployment_detail.release_name), 
                            self.deployment_plan_columns[2]: str(target_release.name.split('-')[1]), 
                            self.deployment_plan_columns[3]: str(rollback_release.name.split('-')[1]),
                            self.deployment_plan_columns[4]: ''
                            }, index=[0])

                        return new_row
                else:    
                    self.release_finder.get_releases(deployment_detail, find_via_stage=self.via_stage)

            except Exception as e:
                logging.error(f'There was an error in the search process. Please continue manually.\nException:{e}')
        else:
            try:
                release_to_update = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage)
                update_manager = UpdateRelease(constants, self.ms_authentication, environment_variables, self.release_finder)

                update_attempt = update_manager.update_release(deployment_detail, release_to_update)
                update_attempt_successful = update_attempt[0]
                update_comment = update_attempt[1]

                if update_attempt_successful:
                    # Check the status of release update
                    logging.info(f'Monitoring update Status - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{environment_variables.RELEASE_STAGE_NAME}')
                    release_updated_successfully = update_manager.get_release_update_result(deployment_detail, release_to_update)

                    if not release_updated_successfully:
                        update_manager.handle_failed_update(deployment_detail, self.via_stage)
                    else:
                        logging.info(f'Release Update Successful - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{environment_variables.RELEASE_STAGE_NAME}')
                else:
                    update_manager.handle_failed_update(deployment_detail, self.via_stage, failure_reason=update_comment)

            except Exception as e:
                logging.error(f'There was an error. Please check their status and continue manually.\nException:{e}')

if __name__ == '__main__':
    startup = Startup()
    t1 = time.perf_counter()

    if environment_variables.SEARCH_ONLY and environment_variables.QUERY != None:
        results = startup.start_request(None)
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(startup.start_request, deployment_plan.deployment_details)
        
    if environment_variables.VIA_STAGE_LATEST_RELEASE or environment_variables.QUERY:
        for row in results:
            if row is not None:
                excel_manager.save_or_concat_file(row, constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH)

    t2 = time.perf_counter()
    logging.info(f'Tasks completed in {t2-t1} seconds')