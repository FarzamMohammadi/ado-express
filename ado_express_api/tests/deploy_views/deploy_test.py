from datetime import datetime
import json
import random
import unittest
from faker import Faker
from mock import patch
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser

from api.deploy_views import deploy
from base.models.DeploymentDetails import DeploymentDetails
from base.models.ReleaseDetails import ReleaseDetails
from base.models.RunConfigurations import RunConfigurations

class Empty:
    pass


class SearchViaLatestRelease(unittest.TestCase):
     
    def setUp(self):
        self.fake = Faker()
        self.factory = RequestFactory()
        
    @patch('ado_express.main.Startup.run_release_deployments')
    @patch('ado_express.main.Startup.load_dependencies', return_value=None)
    @patch('ado_express.main.Startup.initialize_logging', return_value=None)
    @patch('ado_express.main.Startup.remove_crucial_deployments_from_deployment_details', return_value=None)
    @patch('ado_express.main.Startup.get_crucial_deployment_from_deployment_details', return_value=None)
    @patch('ado_express.main.Startup.get_crucial_release_definitions', return_value=None)
    @patch('ado_express.main.Startup.updated_deployment_details_based_on_explicit_inclusion_and_exclusion', return_value=None)
    def test_api_call(self, explicit_release_method_mock, get_crucial_defs_mock, get_crucial_deployments_mock, remove_crucial_deployments_mock, initialize_logging_mock, load_dependencies_mock, run_release_deployments_mock):
            # Arrange
            regular_release_details = DeploymentDetails(self.fake.name(), self.fake.name(), 123, 132, False)
            crucial_release_details = DeploymentDetails(self.fake.name(), self.fake.name(), 123, 132, True)
            run_configurations = RunConfigurations({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),self.fake.name(),True,True,True,self.fake.name(), [crucial_release_details, regular_release_details])
            deployed_release = ReleaseDetails(self.fake.name(), self.fake.name(), self.fake.name(), self.fake.name(), bool(random.getrandbits(1)), datetime.now())

            get_crucial_defs_mock.return_value = [self.fake.name()]
            get_crucial_deployments_mock.return_value = [self.fake.name()] #Doesn't actually matter as long as it's not None
            remove_crucial_deployments_mock.return_value = [self.fake.name()] #Doesn't actually matter as long as it's not None
            run_release_deployments_mock.return_value = deployed_release

            request = self.factory.post('/deploy', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
            request.user = AnonymousUser()

            # Act
            response = deploy(request)

            # Assert
            self.assertEqual(response.data, {'crucial_deployments': json.dumps([deployed_release.__dict__], default=str), 'regular_deployments': json.dumps([deployed_release.__dict__], default=str)})
            self.assertEqual(response.status_code, 200)

    def test_api_call_with_missing_field(self):
            # Arrange
            run_configurations = RunConfigurations({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),self.fake.name(),True,True,False,self.fake.name(), []) # Missing release_details

            request = self.factory.post('/deploy', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
            request.user = AnonymousUser()

            # Act
            response = deploy(request)

            # Assert
            self.assertEqual(response.status_code, 400)