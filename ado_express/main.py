import logging
import os
from datetime import datetime
from pytz import timezone

from packages.authentication import MSAuthentication
from packages.common.constants import Constants
from packages.common.environment_variables import EnvironmentVariables
from packages.utils import DeploymentPlan
from packages.utils.asset_retrievers.release_finder import ReleaseFinder
from packages.utils.release_manager.update_release import UpdateRelease

logging.basicConfig(filename=Constants.LOG_FILE_PATH, encoding='utf-8', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')
logging.info('Message:Starting application')

class Startup:
    constants = Constants()
    deployment_plan = DeploymentPlan(constants)
    environment_variables = EnvironmentVariables()
    ms_authentication = MSAuthentication(environment_variables)
    release_finder = ReleaseFinder(ms_authentication, deployment_plan.deployment_details, environment_variables)

    search_only = environment_variables.SEARCH_ONLY
    search_file_path = constants.SEARCH_RESULTS_FILE_PATH
    via_stage = environment_variables.VIA_STAGE
    via_stage_latest_release = environment_variables.VIA_STAGE_LATEST_RELEASE

    time_format = '%Y-%m-%d %H:%M:%S'
    datetime_now = datetime.now(timezone('US/Eastern'))
    
    def start_request(self):
        if (self.search_only):
            logging.info('Message:Starting the search...')
            try:
                if os.path.isfile(self.search_file_path):
                    with open(self.search_file_path, "a") as file:
                        file.write(f"\n\nNew Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n\n")
                else:
                    with open(self.search_file_path, "a") as file:
                        file.write(f"New Search Results:\nSearched Date & Time:{self.datetime_now.strftime(self.time_format)}\n\n")

                if self.via_stage_latest_release:
                    for deployment_detail in self.deployment_plan.deployment_details:
                        soruce_release = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage)
                        destination_release = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage, rollback=True)

                        with open(self.search_file_path, "a") as file:
                            file.write(f"\n{deployment_detail.release_name} Results:\n") 
                            file.write(f"Release: Release Name: {soruce_release.name} -Based on last release in '{self.environment_variables.VIA_STAGE_SOURCE_NAME}' stage\n") 
                            file.write(f"Rollback: Release Name: {destination_release.name} -Based on last release in '{self.environment_variables.RELEASE_STAGE_NAME}' stage\n")            
           
                else:    
                    self.release_finder.get_releases(find_via_stage=self.via_stage)

            except Exception as e:
                logging.error(f'There was an error in the search process. Please continue manually.\nException:{e}')
        else:
            logging.info('Message:Starting the update...')
            try:
                for deployment_detail in self.deployment_plan.deployment_details:
                    release_to_update = self.release_finder.get_release(deployment_detail, find_via_stage=self.via_stage)
                    update_manager = UpdateRelease(self.constants, self.ms_authentication, self.environment_variables, self.release_finder)

                    update_attempt = update_manager.update_release(deployment_detail, release_to_update)
                    update_attempt_successful = update_attempt[0]
                    update_comment = update_attempt[1]

                    if update_attempt_successful:
                        # Check the status of release update
                        logging.info(f'Message:Monitoring update Status - Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name} Destination Environment:{self.environment_variables.RELEASE_STAGE_NAME}')
                        release_updated_successfully = update_manager.get_release_update_result(deployment_detail, release_to_update)

                        if not release_updated_successfully:
                            update_manager.handle_failed_update(deployment_detail, self.via_stage)
                        else:
                            logging.info(f'Message:Release Update Successful - Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name} Destination Environment:{self.environment_variables.RELEASE_STAGE_NAME}')
                    else:
                        update_manager.handle_failed_update(deployment_detail, self.via_stage, failure_reason=update_comment)

            except Exception as e:
                logging.error(f'There was an error. Please check their status and continue manually.\nException:{e}')

if __name__ == '__main__':
    startup = Startup()
    startup.start_request()