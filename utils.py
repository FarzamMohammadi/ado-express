import pandas as pd

from models import Deployment_Details

def get_data_from_deployment_plan_file():
    release_dataframe = pd.read_excel('./files/deployment-plan.xlsx').apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    deployment_details = []
    
    for inedx, row in release_dataframe.iterrows():
        deployment_details.append(Deployment_Details(row['Project Name'].strip(), row['Release Definition Name'].strip().lower(), row['Release Number'], row['Rollback Number']))

    return deployment_details