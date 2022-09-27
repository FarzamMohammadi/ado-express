import pandas as pd
import time

from models import Deployment_Details
from constants import ENVIRONMENT_STATUSES

def get_data_from_deployment_plan_file():
    release_dataframe = pd.read_excel('./files/deployment-plan.xlsx').apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    deployment_details = []
    
    for index, row in release_dataframe.iterrows():
        deployment_details.append(Deployment_Details(row['Project Name'].strip(), row['Release Name'].strip().lower(), row['Release Number'], row['Rollback Number']))

    return deployment_details

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