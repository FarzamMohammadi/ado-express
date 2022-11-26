from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from packages.common import EnvironmentVariables

class MSAuthentication:

    def __init__(self, environment_variables: EnvironmentVariables):
        self.credentials = BasicAuthentication('', environment_variables.PERSONAL_ACCESS_TOKEN)
        self.connection = Connection(base_url=environment_variables.ORGANIZATION_URL, creds=self.credentials)

        self._build_client = self.connection.clients.get_build_client()
        self._git_client = self.connection.clients.get_git_client()
        self._release_client = self.get_release_client()
        self._release_client_v6 = self.get_release_client(version=6)
        self._work_item_tracking_client = self.connection.clients.get_work_item_tracking_client()
        self._work_client = self.connection.clients.get_work_client()
    
    @property
    def build_client(self):
        return self._build_client

    @property
    def client(self):
        return self._release_client

    @property
    def client_v6(self):
        return self._release_client_v6

    @property
    def git_client(self):
        return self._git_client

    @property
    def work_client(self):
        return self._work_client

    @property
    def work_item_tracking_client(self):
        return self._work_item_tracking_client

    def get_release_client(self, version=None):
        if version is None:
            return self.connection.clients.get_release_client()
        elif version == 6:
            return self.connection.clients_v6_0.get_release_client()