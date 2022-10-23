from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from packages.common import EnvironmentVariables

class MSAuthentication:

    def __init__(self, environment_variables: EnvironmentVariables):
        self.credentials = BasicAuthentication('', environment_variables.PERSONAL_ACCESS_TOKEN)
        self.connection = Connection(base_url=environment_variables.ORGANIZATION_URL, creds=self.credentials)

        self._client = self.get_release_client()
        self._client_v6 = self.get_release_client(version=6)

    @property
    def client(self):
        return self._client

    @property
    def client_v6(self):
        return self._client_v6

    def get_release_client(self, version=None):
        if version is None:
            return self.connection.clients.get_release_client()
        elif version == 6:
            return self.connection.clients_v6_0.get_release_client()