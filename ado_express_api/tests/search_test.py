# from base.models import DeploymentDetails
# from rest_framework import status
# from rest_framework.test import APITestCase
from base.models import RunConfigurations
import unittest
from faker import Faker
from mock import patch
from api.search_views import search_via_query
class Empty:
    pass

class SearchTests(unittest.TestCase):
    
    @patch('packages.authentication.MSAuthentication', return_value=None)  
    @patch('packages.utils.asset_retrievers.work_item_manager.work_item_manager.WorkItemManager', return_value=None)  
    @patch('packages.utils.asset_retrievers.release_finder.ReleaseFinder', return_value=None)
    @patch('main.Startup', return_value=None)  
    def test_query_run(self, ms_authentication, work_item_manager, release_finder, startup):
        
            '''
            pass runConfigs

            run query search

            return deploymentdetails
            '''
            # Arrange
            fake = Faker()
            run_configurations = RunConfigurations(None,None,fake.name(),fake.name(),fake.name(),fake.name(),fake.name(),True,True,fake.name(),None)
            target_releases = {'r1':'1', 'r2':'2'}
            rollback_releases = {'r0':'0', 'r01':'01'}

            work_item_manager.get_query_build_ids().return_value=fake.name()
            release_finder.get_releases_via_builds().return_value=target_releases
            release_finder.get_releases_via_builds().return_value=rollback_releases
            
            

            # Act
            search_via_query(request)
