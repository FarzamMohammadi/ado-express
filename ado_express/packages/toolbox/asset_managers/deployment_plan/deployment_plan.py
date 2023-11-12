import numpy as np
import pandas as pd

from ado_express.packages.shared.constants import Constants
from ado_express.packages.shared.environment_variables import \
    EnvironmentVariables
from ado_express.packages.shared.models import DeploymentDetails


class DeploymentPlan():

    def __init__(self, constants: Constants, environment_variables: EnvironmentVariables):
        self.constants = constants
        self.environment_variables = environment_variables


    def get_data_from_deployment_plan_file(self):
        file_path = self.constants.DEPLOYMENT_PLAN_FILE_PATH
        
        release_dataframe = pd.read_excel(file_path).replace(np.nan, None, regex=True).apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        deployment_details = []
        
        for index, row in release_dataframe.iterrows():
            
            deployment_details.append(DeploymentDetails(row['Project Name'].strip(), row['Release Name'].strip().lower(), row['Release Number'], row['Rollback Number'], self.get_validated_crucial_input(row['Crucial'])))

        return deployment_details

    def get_validated_crucial_input(self, str_input):
        true_types = ["true", "1", "t", "yes", "y"]

        if str_input and str(str_input).strip().lower() in true_types:
            return True

        return False