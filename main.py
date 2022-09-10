import logging
import os

from azure.devops.connection import Connection
from azure.devops.v5_1.release.models import ReleaseEnvironmentUpdateMetadata
from dotenv import load_dotenv
from msrest.authentication import BasicAuthentication

from utils import get_data_from_deployment_plan_file

logging.basicConfig(filename='deployment.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Starting release stage updates...')

# Get environment variables
load_dotenv()

personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
organization_url = os.getenv('ORGANIZATION_URL')
release_stage_name = os.getenv('RELEASE_STAGE_NAME')
release_name_format = os.getenv('RELEASE_NAME_FORMAT')

# Get deployment details from excel file
deployments_to_update = get_data_from_deployment_plan_file() 

# Auth & connection creation
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get clients
release_client = connection.clients.get_release_client()
release_client_v6 = connection.clients_v6_0.get_release_client()

try:
    for deployment_to_update in deployments_to_update:
        # Gets release definitions names 
        release_definitions = release_client.get_release_definitions(project=deployment_to_update.release_project_name) 

        for definition in release_definitions.value:
            if (str(definition.name).lower() == deployment_to_update.release_definition_name):
                release_definition = definition

        # Get release id from release to know which needs to be deployed to new env
        releases = release_client.get_releases(project=deployment_to_update.release_project_name, definition_id=release_definition.id) 
        
        for release in releases.value:
            if str(release.name).lower() == (release_name_format.split('$')[0].lower() + str(deployment_to_update.release_number)):
                release_to_update = release
                break

        # Get specified release environments
        release_to_update_data = release_client.get_release(project=deployment_to_update.release_project_name, release_id=release_to_update.id)
        
        for environment in release_to_update_data.environments:
            if (str(environment.name).lower() == release_stage_name.lower()):
                environment_to_update_release_to = environment

        environment_update_data = ReleaseEnvironmentUpdateMetadata(comment='', status=2)
        release_client_v6.update_release_environment(environment_update_data=environment_update_data, project=deployment_to_update.release_project_name, release_id=release_to_update_data.id, environment_id=environment_to_update_release_to.id)
        
        logging.info(f'Attempted environment update for release:{deployment_to_update.release_project_name} of project:{deployment_to_update.release_project_name} to {release_stage_name}.\nPlease manually check the status of the release to ensure the update was successful.')
except Exception as e:
    logging.error(f'There was an error updating the deployments. Please check their status and continue manually.\nException:{e}')



