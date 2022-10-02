import datetime
import logging
import os
import time
from dotenv import load_dotenv
import numpy as np
import pandas as pd

from models import Deployment_Details
from constants import ENVIRONMENT_STATUSES
from azure.devops.v5_1.release.models import ReleaseEnvironmentUpdateMetadata

# Get environment variables
load_dotenv()

release_stage_name = os.getenv('RELEASE_STAGE_NAME')
release_name_format = os.getenv('RELEASE_NAME_FORMAT')

def find_matching_release(release_client, deployment_to_update, rollback=False):
    if not rollback:
        release_number = deployment_to_update.release_number
    else: 
        release_number = deployment_to_update.release_rollback

    # Gets release definitions names 
    release_definitions = release_client.get_release_definitions(project=deployment_to_update.release_project_name) 
    
    for definition in release_definitions.value:
            if (str(definition.name).lower() == str(deployment_to_update.release_name).lower()):
                release_definition = definition

    # Get release id from release to know which needs to be deployed to new env
    releases = release_client.get_releases(project=deployment_to_update.release_project_name, definition_id=release_definition.id) 
    
    for release in releases.value:
        if str(release.name).lower() == (release_name_format.split('$')[0].lower() + str(release_number)):
            return release

def get_data_from_deployment_plan_file():
    release_dataframe = pd.read_excel('./files/deployment-plan.xlsx').replace(np.nan, None, regex=True).apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    deployment_details = []
    
    for index, row in release_dataframe.iterrows():
        deployment_details.append(Deployment_Details(row['Project Name'].strip(), row['Release Name'].strip().lower(), row['Release Number'], row['Rollback Number'], row['Crucial']))

    return deployment_details

def handle_failed_update(deployment_to_update, release_client, release_client_v6, release_to_update_data, reason=None):
    if reason is not None:
        logging.error(f'Message:Release Update Unsuccessful - Reason: {reason} - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    else:
        logging.error(f'Message:Release Update Unsuccessful - Reason: Please check logs - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    if deployment_to_update.is_crucial is True:
        logging.error(f'Message:Release update was crucial. Now attempting rollback. - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
       
        # Search projects to find specified release for roll back
        matching_release_to_rollback = find_matching_release(release_client, deployment_to_update, rollback=True)

        if matching_release_to_rollback is None: 
            raise Exception(f'Unable to find matching roll back update. Stopping the process. - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        roll_back_release(release_client, deployment_to_update, matching_release_to_rollback, release_client_v6)

        raise Exception('A curcial release update failed. Roll back was attempted. Now, stopping the process.')
    else:
        logging.info(f'Message:The failed release update was not curcial. Now moving on to the next update... Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

def release_updated_successfuly(release_client, project_name, release_id):
    updated_successfully = False
    update_complete = False

    while not update_complete:
        release_to_update_data = release_client.get_release(project=project_name, release_id=release_id)
        for environment in release_to_update_data.environments:
                if (str(environment.name).lower() == release_stage_name.lower()):
                    if environment.status in ENVIRONMENT_STATUSES.SUCCEEDED: 
                        updated_successfully = True
                        update_complete = True
                        break
                    elif environment.status in ENVIRONMENT_STATUSES.FAILED:
                        update_complete = True
                        break       
        time.sleep(5)
                        
    return updated_successfully
    
def roll_back_release(release_client, deployment_to_update, matching_release_to_rollback, release_client_v6):
        # Get specified release environments
        release_to_update_data = release_client.get_release(project=deployment_to_update.release_project_name, release_id=matching_release_to_rollback.id)

        for environment in release_to_update_data.environments:
            if (str(environment.name).lower() == release_stage_name.lower()):
                matching_release_environment = environment
        
        if matching_release_environment is not None:
            if matching_release_environment.status not in ENVIRONMENT_STATUSES.IN_PROGRESS:
                # Rollback Release
                comment = 'Rolled back automatically due to failed update via Ado-Express'
                update_release_environment(comment, release_client_v6, deployment_to_update, release_to_update_data, matching_release_environment)
            else: 
                logging.info(f'Message:Release is already rolling back - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                
            # Check the status of release update
            logging.info(f'Message:Monitoring rollback Status - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            updated_successfully = release_updated_successfuly(release_client, deployment_to_update.release_project_name, release_to_update_data.id)

            if updated_successfully:
                logging.info(f'Message:Release roll back Successful - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                return

        logging.error(f'Message:Unable to roll back. Please check this release manually. - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


def update_release(release_client, deployment_to_update, matching_release_to_update, release_client_v6):
        # Get specified release environments
        release_to_update_data = release_client.get_release(project=deployment_to_update.release_project_name, release_id=matching_release_to_update.id)

        for environment in release_to_update_data.environments:
            if (str(environment.name).lower() == release_stage_name.lower()):
                matching_release_environment = environment
        
        if matching_release_environment is not None:
            if matching_release_environment.status not in ENVIRONMENT_STATUSES.IN_PROGRESS:
                # Update Release
                comment = 'Deployed automatically via Ado-Express'
                update_release_environment(comment, release_client_v6, deployment_to_update, release_to_update_data, matching_release_environment)
            else: 
                logging.info(f'Message:Release is already updating - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                
            # Check the status of release update
            logging.info(f'Message:Monitoring update Status - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            updated_successfully = release_updated_successfuly(release_client, deployment_to_update.release_project_name, release_to_update_data.id)

            if not updated_successfully:
                handle_failed_update(deployment_to_update, release_client, release_client_v6, release_to_update_data)
            else:
                logging.info(f'Message:Release Update Successful - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} Destination Environment:{release_stage_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        else: 
            failure_reason = f'Destination Environment "{release_stage_name}" not found'
            handle_failed_update(deployment_to_update, release_client, release_client_v6, release_to_update_data, failure_reason)

def update_release_environment(comment, release_client_v6, deployment_to_update, release_to_update_data, matching_release_environment):
    environment_update_data = ReleaseEnvironmentUpdateMetadata(comment, status=2)
    return release_client_v6.update_release_environment(environment_update_data=environment_update_data, project=deployment_to_update.release_project_name, release_id=release_to_update_data.id, environment_id=matching_release_environment.id)
            
