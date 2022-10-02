import logging
import os
import datetime

from azure.devops.connection import Connection
from azure.devops.v5_1.release.models import ReleaseEnvironmentUpdateMetadata
from dotenv import load_dotenv
from msrest.authentication import BasicAuthentication

from utils import get_data_from_deployment_plan_file, handle_failed_update, release_updated_successfuly
from constants import ENVIRONMENT_STATUSES

logging.basicConfig(filename='deployment_error.log', encoding='utf-8', level=logging.INFO)
logging.info(f'Message:Starting release stage updates - Date & Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

# Get environment variables
load_dotenv()

personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
organization_url = os.getenv('ORGANIZATION_URL')
release_stage_name = os.getenv('RELEASE_STAGE_NAME')
release_name_format = os.getenv('RELEASE_NAME_FORMAT')

# Get deployment details from excel file
releases_to_update = get_data_from_deployment_plan_file() 

# Auth & connection creation
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get clients
release_client = connection.clients.get_release_client()
release_client_v6 = connection.clients_v6_0.get_release_client()

try:
    for deployment_to_update in releases_to_update:
        # Gets release definitions names 
        release_definitions = release_client.get_release_definitions(project=deployment_to_update.release_project_name) 

        for definition in release_definitions.value:
            if (str(definition.name).lower() == deployment_to_update.release_name):
                release_definition = definition

        # Get release id from release to know which needs to be deployed to new env
        releases = release_client.get_releases(project=deployment_to_update.release_project_name, definition_id=release_definition.id) 
        
        for release in releases.value:
            if str(release.name).lower() == (release_name_format.split('$')[0].lower() + str(deployment_to_update.release_number)):
                matching_release_to_update = release
                break

        # Get specified release environments
        release_to_update_data = release_client.get_release(project=deployment_to_update.release_project_name, release_id=matching_release_to_update.id)

        for environment in release_to_update_data.environments:
            if (str(environment.name).lower() == release_stage_name.lower()):
                matching_release_environment = environment
        
        if matching_release_environment is not None:
            if matching_release_environment.status not in ENVIRONMENT_STATUSES.IN_PROGRESS:
                # Update Release
                environment_update_data = ReleaseEnvironmentUpdateMetadata(comment='', status=2)
                update = release_client_v6.update_release_environment(environment_update_data=environment_update_data, project=deployment_to_update.release_project_name, release_id=release_to_update_data.id, environment_id=matching_release_environment.id)
            else: logging.info(f'Message:Release is already updating - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

            # Check the status of release update
            logging.info(f'Message:Monitoring Update Status - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            updated_successfully = release_updated_successfuly(release_client, deployment_to_update.release_project_name, release_stage_name, matching_release_to_update.id)

            if not updated_successfully:
                handle_failed_update(deployment_to_update)
            else:
                logging.info(f'Message:Release Update Successful - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        else: 
            failure_reason = f'Destination Environment "{release_stage_name}" not found'
            handle_failed_update(deployment_to_update, failure_reason)
            continue
            
except Exception as e:
    logging.error(f'There was an error updating the deployments. Please check their status and continue manually.\nException:{e}')



