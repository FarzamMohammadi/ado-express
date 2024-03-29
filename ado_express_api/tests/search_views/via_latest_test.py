import json
import unittest
from faker import Faker
from mock import patch
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser

from api.search_views import search_via_latest_release
from base.models.DeploymentDetail import DeploymentDetail
from base.models.RunConfiguration import RunConfiguration


class Empty:
    pass


class SearchViaLatestRelease(unittest.TestCase):
     
    def setUp(self):
        self.fake = Faker()
        self.factory = RequestFactory()
        
    @patch('ado_express.main.Startup.get_deployment_detail_from_latest_release')
    @patch('ado_express.main.Startup.load_dependencies', return_value=None)
    @patch('ado_express.main.Startup.initialize_logging', return_value=None)
    def test_api_call(self, initialize_logging_mock, load_dependencies_mock, get_deployment_detail_from_latest_release_mock):
            # Arrange
            release_details = DeploymentDetail(self.fake.name(), self.fake.name(), 123, 132, False)
            run_configurations = RunConfiguration({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),self.fake.name(),True,True,True,self.fake.name(), [release_details, release_details, release_details])

            deployment = Empty()
            deployment.release_project_name = self.fake.name()
            deployment.release_name = self.fake.name()
            deployment.release_number = self.fake.random_int()
            deployment.release_rollback = self.fake.random_int()
            deployment.is_crucial = False

            get_deployment_detail_from_latest_release_mock.return_value = deployment

            request = self.factory.post('/search/via-latest', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
            request.user = AnonymousUser()

            # Act
            response = search_via_latest_release(request)

            # Assert
            self.assertEqual(response.data, {'releases': json.dumps([deployment.__dict__, deployment.__dict__, deployment.__dict__])})
            self.assertEqual(response.status_code, 200)

    def test_api_call_with_missing_field(self):
            # Arrange
            release_details = DeploymentDetail(self.fake.name(), None, None, None, False) # Missing release_name
            run_configurations = RunConfiguration({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),self.fake.name(),True,True,False,self.fake.name(), [release_details])

            request = self.factory.post('/search/via-latest', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
            request.user = AnonymousUser()

            # Act
            response = search_via_latest_release(request)

            # Assert
            self.assertEqual(response.status_code, 400)