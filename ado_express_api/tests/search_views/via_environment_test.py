import datetime
import json
import unittest
from faker import Faker
from mock import patch
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from base.models.ReleaseDetail import ReleaseDetail

from api.search_views import search_via_release_environment
from base.models.DeploymentDetail import DeploymentDetail
from base.models.RunConfiguration import RunConfiguration


class Empty:
    pass


class SearchViaLatestRelease(unittest.TestCase):
     
    def setUp(self):
        self.fake = Faker()
        self.factory = RequestFactory()
        
    @patch('ado_express.main.Startup.search_and_log_details_only')
    @patch('ado_express.main.Startup.load_dependencies', return_value=None)
    @patch('ado_express.main.Startup.initialize_logging', return_value=None)
    def test_api_call(self, initialize_logging_mock, load_dependencies_mock, search_and_log_details_only_mock):
            # Arrange
            release_details = DeploymentDetail(self.fake.name(), self.fake.name(), 123, 132, False)
            run_configurations = RunConfiguration({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),self.fake.name(),True,True,True,self.fake.name(), [release_details, release_details])
            release = ReleaseDetail(release_details.release_project_name, release_details.release_name, self.fake.name(), self.fake.name(), True, datetime.datetime.now())

            returned_releases = [release, release, release]
            search_and_log_details_only_mock.return_value = returned_releases

            request = self.factory.post('/search/via-environment', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
            request.user = AnonymousUser()

            returned_results = [dict({'release_definition': release_details.release_name, 'results': [release.__dict__ for release in returned_releases]}), 
                                dict({'release_definition': release_details.release_name, 'results': [release.__dict__ for release in returned_releases]})]

            # Act
            response = search_via_release_environment(request)

            # Assert
            self.assertEqual(response.data, {'releases': json.dumps(returned_results, default=str) })
            self.assertEqual(response.status_code, 200)

    def test_api_call_with_missing_field(self):
            # Arrange
            release_details = DeploymentDetail(self.fake.name(), None, None, None, False) # Missing release_name
            run_configurations = RunConfiguration({},[],self.fake.name(),self.fake.name(),[self.fake.name()],self.fake.name(),self.fake.name(),True,True,False,self.fake.name(), [release_details])

            request = self.factory.post('/search/via-environment', json.dumps(run_configurations.to_dict_with_lowercase_keys()), content_type='application/json')
            request.user = AnonymousUser()

            # Act
            response = search_via_release_environment(request)

            # Assert
            self.assertEqual(response.status_code, 400)