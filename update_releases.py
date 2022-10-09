import logging
import os
import datetime

from azure.devops.connection import Connection
from dotenv import load_dotenv
from msrest.authentication import BasicAuthentication

from utils import find_matching_release, get_data_from_deployment_plan_file, update_release

logging.basicConfig(filename='deployment.log', encoding='utf-8', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')
logging.info(f'Message:Starting release stage updates')

# Get environment variables
load_dotenv()

personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
organization_url = os.getenv('ORGANIZATION_URL')

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
        # Search projects to find specified release
        matching_release_to_update = find_matching_release(release_client, deployment_to_update)
        
        if matching_release_to_update is None: 
            raise Exception(f'Unable to find matching release to update. Stopping the process. - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name}')
        
        update_release(release_client, deployment_to_update, matching_release_to_update, release_client_v6)

except Exception as e:
    logging.error(f'There was an error updating the deployments. Please check their status and continue manually.\nException:{e}')



