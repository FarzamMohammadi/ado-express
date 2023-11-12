import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from ado_express.packages.shared import (Constants, DeploymentDetails,
                                         environment_variables)
from ado_express.packages.toolbox import DeploymentPlan
from ado_express.tests.test_helpers.mock_provider.mock_environment_variables import \
    MockEnvironmentVariables


@patch.object(environment_variables, 'EnvironmentVariables', new=MockEnvironmentVariables)
class TestDeploymentPlan(unittest.TestCase):

    def setUp(self):
        self.constants = Constants()
        self.deployment_plan = DeploymentPlan(self.constants, MockEnvironmentVariables())

    from unittest.mock import MagicMock

    @patch('pandas.read_excel')
    def test_get_data_from_deployment_plan_file(self, mock_read_excel):
        data = {
            'Project Name': 'Test Project',
            'Release Name': 'Test Release',
            'Release Number': '1',
            'Rollback Number': '0',
            'Crucial': 'yes'
        }

        df = pd.DataFrame([data])

        transformed_df = df.replace(np.nan, None, regex=True)
        transformed_df = transformed_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        mock_read_excel.return_value = transformed_df

        result = self.deployment_plan.get_data_from_deployment_plan_file()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], DeploymentDetails)
        self.assertEqual(result[0].release_project_name, 'Test Project')
        self.assertEqual(result[0].release_name, 'test release')
        self.assertEqual(result[0].release_number, '1')
        self.assertEqual(result[0].release_rollback, '0')
        self.assertTrue(result[0].is_crucial)

    def test_get_validated_crucial_input(self):
        self.assertEqual(self.deployment_plan.get_validated_crucial_input('yes'), True)
        self.assertEqual(self.deployment_plan.get_validated_crucial_input('no'), False)

if __name__ == '__main__':
    unittest.main()