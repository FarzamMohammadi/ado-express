from asyncio import exceptions
import datetime
import logging
import time
import numpy as np
import pandas as pd

from models import Deployment_Details
from constants import ENVIRONMENT_STATUSES

def get_data_from_deployment_plan_file():
    release_dataframe = pd.read_excel('./files/deployment-plan.xlsx').replace(np.nan, None, regex=True).apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    deployment_details = []
    
    for index, row in release_dataframe.iterrows():
        deployment_details.append(Deployment_Details(row['Project Name'].strip(), row['Release Name'].strip().lower(), row['Release Number'], row['Rollback Number'], row['Crucial']))

    return deployment_details

def handle_failed_update(deployment_to_update,  reason=None):
    if reason is not None:
        logging.error(f'Message:Release Update Unsuccessful - Reason: {reason} - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    else:
        logging.error(f'Message:Release Update Unsuccessful - Reason: Please check logs - Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    if deployment_to_update.is_crucial is True:
        raise Exception('A curcial release update failed. Stopping process...')
    else:
        logging.info(f'Message:The failed release update was not curcial. Now moving on to the next update... Project:{deployment_to_update.release_project_name} Release:{deployment_to_update.release_name} At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

def release_updated_successfuly(release_client, project_name, stage_name, release_id):
    updated_successfully = False
    update_complete = False

    while not update_complete:
        release_to_update_data = release_client.get_release(project=project_name, release_id=release_id)
        for environment in release_to_update_data.environments:
                if (str(environment.name).lower() == stage_name.lower()):
                    if environment.status in ENVIRONMENT_STATUSES.SUCCEEDED: 
                        updated_successfully = True
                        update_complete = True
                        break
                    elif environment.status in ENVIRONMENT_STATUSES.FAILED:
                        update_complete = True
                        break       
        time.sleep(5)
                        
    return updated_successfully