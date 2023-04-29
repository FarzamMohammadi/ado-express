import logging
import time

from azure.devops.v5_1.release.models import ReleaseEnvironmentUpdateMetadata

from ado_express.packages.authentication import MSAuthentication
from ado_express.packages.common.constants import Constants
from ado_express.packages.common.enums import ReleaseEnvironmentStatuses
from ado_express.packages.common.environment_variables import \
    EnvironmentVariables
from ado_express.packages.utils.asset_retrievers import ReleaseFinder
from ado_express.packages.utils.asset_retrievers.release_environment_finder import \
    ReleaseEnvironmentFinder


class UpdateRelease:
    
    def __init__(self, constants: Constants, ms_authentication: MSAuthentication, environment_variables: EnvironmentVariables, release_finder: ReleaseFinder):
        self.constants = constants
        self.ms_authentication = ms_authentication
        self.release_client = ms_authentication.client
        self.release_client_v6 = ms_authentication.client_v6
        self.environment_variables = environment_variables
        self.release_finder = release_finder

        
    def update_release(self, deployment_detail, release_to_update):
        # Get specified release environments
        release_environment_finder = ReleaseEnvironmentFinder(self.ms_authentication, self.environment_variables)
        matching_release_environment = release_environment_finder.get_release_environment(deployment_detail, release_to_update.id)
        
        if matching_release_environment is not None:
            
            if matching_release_environment.status not in ReleaseEnvironmentStatuses.InProgress:
                # Update Release
                comment = 'Deployed automatically via ADO-Express (https://github.com/FarzamMohammadi/ado-express)'
                update_result = self.update_release_environment(comment, deployment_detail, release_to_update, matching_release_environment)
                logging.info(f'Update triggered - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{self.environment_variables.RELEASE_TARGET_ENV}')
            else: 
                logging.info(f'Release is already updating - Project:{deployment_detail.release_project_name} Release Definition:{deployment_detail.release_name} Release:{release_to_update.name} Environment:{self.environment_variables.RELEASE_TARGET_ENV}')
            
            return (True, None), matching_release_environment
        else: 
            failure_reason = f'Destination Release Environment "{self.environment_variables.RELEASE_TARGET_ENV}" not found'
            return (False, failure_reason), matching_release_environment


    def get_release_update_result(self, deployment_detail, release_to_update):
        updated_successfully = False
        update_complete = False

        while not update_complete:
            release_to_update_data = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release_to_update.id)
            for environment in release_to_update_data.environments:
                if (str(environment.name).lower() == self.environment_variables.RELEASE_TARGET_ENV.lower()):
                    if environment.status in ReleaseEnvironmentStatuses.Succeeded: 
                        updated_successfully = True
                        update_complete = True
                        break
                    elif environment.status in ReleaseEnvironmentStatuses.Failed:
                        update_complete = True
                        break       
            time.sleep(5)
                            
        return updated_successfully

    def update_release_environment(self, comment, deployment_detail, release_to_update, matching_release_environment):
        update_metadata = ReleaseEnvironmentUpdateMetadata(comment, status=2)
        return self.release_client_v6.update_release_environment(environment_update_data=update_metadata, project=deployment_detail.release_project_name, release_id=release_to_update.id, environment_id=matching_release_environment.id)


    def handle_failed_update(self, deployment_detail, via_env=False, failure_reason=None):
        if failure_reason is not None:
            logging.error(f'Release Update Unsuccessful - Reason: {failure_reason} - Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name}')
        else:
            logging.error(f'Release Update Unsuccessful - Reason: Please check logs - Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name}')

        if deployment_detail.is_crucial is True:
            logging.error(f'Release update was crucial. Now attempting rollback. - Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name}')
        
            # Search projects to find specified release for roll back
            release_to_rollback = self.release_finder.get_release(deployment_detail, find_via_env=via_env, rollback=True)

            if release_to_rollback is None:
                raise Exception(f'Unable to find matching roll back update. Stopping the process. - Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name}')
            
            self.roll_back_release(deployment_detail, release_to_rollback)

            raise Exception('A crucial release update failed. Roll back was attempted. Now, stopping the process.')
        else:
            logging.info(f'The failed release update was not crucial. Continuing... Project:{deployment_detail.release_project_name} Release:{deployment_detail.release_name}')
    
    def roll_back_release(self, deployment_detail, release_to_rollback):
        release_target_env = self.environment_variables.RELEASE_TARGET_ENV
        release_name = deployment_detail.release_name
        release_project_name = deployment_detail.release_project_name
        release_log_details = f'Project:{release_project_name} Release:{release_name} Environment:{release_target_env}'

        # Get specified release environments
        release_to_update = self.release_client.get_release(project=release_project_name, release_id=release_to_rollback.id)
        
        for environment in release_to_update.environments:
            if (str(environment.name).lower() == self.environment_variables.RELEASE_TARGET_ENV.lower()):
                matching_release_environment = environment
        
        if matching_release_environment is not None:
            if matching_release_environment.status not in ReleaseEnvironmentStatuses.InProgress:
                # Rollback Release
                comment = 'Rolled back automatically due to failed update via Ado-Express'
                self.update_release_environment(comment, deployment_detail, release_to_update, matching_release_environment)
            else: 
                logging.info(f'Release is already rolling back - {release_log_details}')
                
            # Check the status of release update
            logging.info(f'Monitoring rollback Status - {release_log_details}')
            updated_successfully = self.get_release_update_result(deployment_detail, release_to_update)

            if updated_successfully:
                logging.info(f'Release roll back Successful - {release_log_details}')
                return

        logging.error(f'Unable to roll back. Please check this release manually. - {release_log_details}')