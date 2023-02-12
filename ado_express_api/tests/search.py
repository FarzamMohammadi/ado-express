from base.models import DeploymentDetails
from rest_framework import status
from rest_framework.test import APITestCase

class SearchTestCases(APITestCase):

    def test_query_run(self):
        data = {}