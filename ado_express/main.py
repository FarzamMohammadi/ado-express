import concurrent.futures
import logging
import os
import time
from datetime import datetime

from packages.authentication import MSAuthentication
from packages.common.constants import Constants
from packages.common.environment_variables import EnvironmentVariables
from packages.utils import DeploymentPlan
from packages.utils.asset_retrievers.release_finder import ReleaseFinder
from packages.utils.release_manager.update_release import UpdateRelease
from pytz import timezone

logging.basicConfig(filename=Constants.LOG_FILE_PATH, encoding='utf-8', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')
logging.info('Message:Starting application')

constants = Constants()
deployment_plan = DeploymentPlan(constants)

class Startup:

    def __init__(self):
        self.environment_variables = EnvironmentVariables()
        self.ms_authentication = MSAuthentication(self.environment_variables)
        self.release_finder = ReleaseFinder(self.ms_authentication, deployment_plan.deployment_details, self.environment_variables)

        self.search_only = self.environment_variables.SEARCH_ONLY
        self.search_file_path = constants.SEARCH_RESULTS_FILE_PATH
        self.via_stage = self.environment_variables.VIA_STAGE
        self.via_stage_latest_release = self.environment_variables.VIA_STAGE_LATEST_RELEASE

        self.time_format = '%Y-%m-%d %H:%M:%S'
        self.datetime_now = datetime.now(timezone('US/Eastern'))

        # Start Log
        if self.search_only:
            logging.info('Message:Starting the search...')
                
            if os.path.isfile(self.search_file_path):
                with open(self.search_file_path, "a") as file:
                    file.write(f"\n\nNew Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n")
            else:
                with open(self.search_file_path, "a") as file:
                    file.write(f"New Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n")
        else:
            logging.info('Message:Starting the update...')
        
    
    def start_request(self, deployment_detail):
        if self.search_only:
            try:
                if self.via_stage_latest_release:
                    soruce_release = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage)
                    destination_release = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage, rollback=True)

                    with open(self.search_file_path, "a") as file:
                        file.write(f"""
                        \n{deployment_detail.release_name} Results:
                        Target Release: {soruce_release.name} (Based on last release in '{self.environment_variables.VIA_STAGE_SOURCE_NAME}' stage)
                        Rollback Release: {destination_release.name} (Based on last release in '{self.environment_variables.RELEASE_STAGE_NAME}' stage)
                        """)
                else:    
                    self.release_finder.get_releases(deployment_detail, find_via_stage=self.via_stage)

            except Exception as e:
                logging.error(f'There was an error in the search process. Please continue manually.\nException:{e}')
        else:
            try:
                release_to_update = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage)
                update_manager = UpdateRelease(constants, self.ms_authentication, self.environment_variables, self.release_finder)

                update_attempt = update_manager.update_release(deployment_detail, release_to_update)
                update_attempt_successful = update_attempt[0]
                update_comment = update_attempt[1]

                if update_attempt_successful:
                    # Check the status of release update
                    logging.info(f'Message:Monitoring update Status - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{self.environment_variables.RELEASE_STAGE_NAME}')
                    release_updated_successfully = update_manager.get_release_update_result(deployment_detail, release_to_update)

                    if not release_updated_successfully:
                        update_manager.handle_failed_update(deployment_detail, self.via_stage)
                    else:
                        logging.info(f'Message:Release Update Successful - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{self.environment_variables.RELEASE_STAGE_NAME}')
                else:
                    update_manager.handle_failed_update(deployment_detail, self.via_stage, failure_reason=update_comment)

            except Exception as e:
                logging.error(f'There was an error. Please check their status and continue manually.\nException:{e}')

if __name__ == '__main__':
    startup = Startup()
    t1 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(startup.start_request, deployment_plan.deployment_details)
    
    t2 = time.perf_counter()
    logging.info(f'Message:Tasks completed in {t2-t1} seconds')