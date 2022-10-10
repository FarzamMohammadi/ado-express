import numpy as np
import pandas as pd

from packages.common.constants import Constants
from packages.common.models import DeploymentDetails

class DeploymentPlan():

    def __init__(self, constants: Constants):
        self.constants = constants
        self._deployment_details = self.get_data_from_deployment_plan_file()

    @property
    def deployment_details(self):
        return self._deployment_details

    def get_data_from_deployment_plan_file(self):
        
        release_dataframe = pd.read_excel(self.constants.DEPLOYMENT_PLAN_FILE_PATH).replace(np.nan, None, regex=True).apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        deployment_details = []
        
        for index, row in release_dataframe.iterrows():
            deployment_details.append(DeploymentDetails(row['Project Name'].strip(), row['Release Name'].strip().lower(), row['Release Number'], row['Rollback Number'], row['Crucial']))

        return deployment_details