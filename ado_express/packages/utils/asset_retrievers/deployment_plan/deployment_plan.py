import numpy as np
import pandas as pd

from packages.common.constants import Constants
from packages.common.environment_variables import EnvironmentVariables
from packages.common.models import DeploymentDetails

class DeploymentPlan():

    def __init__(self, constants: Constants, environment_variables: EnvironmentVariables):
        self.constants = constants
        self.environment_variables = environment_variables
        self._deployment_details = self.get_data_from_deployment_plan_file()

    @property
    def deployment_details(self):
        return self._deployment_details

    def get_data_from_deployment_plan_file(self):
        file_path = self.constants.SEARCH_RESULTS_DEPLOYMENT_PLAN_FILE_PATH if self.environment_variables.USE_SEARCH_RESULTS else self.constants.DEPLOYMENT_PLAN_FILE_PATH
        
        release_dataframe = pd.read_excel(file_path).replace(np.nan, None, regex=True).apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        deployment_details = []
        
        for index, row in release_dataframe.iterrows():
            deployment_details.append(DeploymentDetails(row['Project Name'].strip(), row['Release Name'].strip().lower(), row['Release Number'], row['Rollback Number'], row['Crucial']))

        return deployment_details