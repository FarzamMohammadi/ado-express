import json
import unittest
from faker import Faker
from mock import patch
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser

from api.search_views import search_via_query
from base.models.RunConfigurations import RunConfigurations


class Empty:
    pass


class SearchViaQuery(unittest.TestCase):
     
    def setUp(self):
        self.fake = Faker()
        self.factory = RequestFactory()
        
    @patch('ado_express.main.Startup.get_deployment_details_from_query')
    @patch('ado_express.main.Startup.load_dependencies', return_value=None)
    @patch('ado_express.main.Startup.initialize_logging', return_value=None)
    def test_api_call(self, initialize_logging_mock, load_dependencies_mock, get_deployment_details_from_query_mock):
            # Arrange
            run_configurations = RunConfigurations({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),self.fake.name(),True,True,False,self.fake.name(), [])

            deployment = Empty()
            deployment.release_project_name = self.fake.name()
            deployment.release_name = self.fake.name()
            deployment.release_number = self.fake.random_int()
            deployment.release_rollback = self.fake.random_int()
            deployment.is_crucial = False

            deployment_details = [deployment, deployment, deployment]
            get_deployment_details_from_query_mock.return_value = deployment_details

            request = self.factory.post('/search/query', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
            request.user = AnonymousUser()

            # Act
            response = search_via_query(request)

            # Assert
            self.assertEqual(response.data, {'releases': json.dumps([ob.__dict__ for ob in deployment_details])})
            self.assertEqual(response.status_code, 200)
    
    def test_api_call_with_missing_fields(self):
        # Arrange
        run_configurations = RunConfigurations({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),"",True,True,False,"", [])

        request = self.factory.post('/search/query', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
        request.user = AnonymousUser()

        # Act
        response = search_via_query(request)

        # Assert
        self.assertEqual(response.status_code, 400)
