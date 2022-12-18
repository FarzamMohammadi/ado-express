import os
import pandas as pd

from typing import List

from packages.common.models import DeploymentDetails

class ExcelManager:

    def __init__(self):
        self.pd = pd

    def align_text(self, df: pd.DataFrame, position='center'):
        return df.style.set_properties(**{'text-align': position})
    
    def create_dataframe(self, file_headers: List[str] = None):
        df = self.pd.DataFrame()

        if file_headers:
            for index, name in enumerate(file_headers):
                df.insert(loc=index, column=str(name), value=None)

        return df

    def convert_deplyoment_detail_to_excel_row(self, file_headers: List[str], deployment_details: DeploymentDetails):
        return self.pd.DataFrame({
                file_headers[0]: deployment_details.release_project_name, 
                file_headers[1]: deployment_details.release_name, 
                file_headers[2]: deployment_details.release_number,
                file_headers[3]: deployment_details.release_rollback,
                file_headers[4]: deployment_details.is_crucial
                }, index=[0])

    def insert_row(self, df, new_df: pd.DataFrame):
        return pd.concat([df, new_df], axis=0)
    
    def save_or_concat_file(self, df: pd.DataFrame, file_path, starting_search=False):
        # Create new file if search is just beginning
        if not starting_search and os.path.isfile(file_path):
            existing_deployment_plan = pd.read_excel(file_path)
            new_df = pd.concat([df, existing_deployment_plan], ignore_index=True)
            return self.align_text(new_df).to_excel(file_path, index=False)
        else:
            return self.align_text(df).to_excel(file_path, index=False)

