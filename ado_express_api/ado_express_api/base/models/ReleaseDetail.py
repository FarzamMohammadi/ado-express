import datetime


class ReleaseDetail:
    """
    :param release_project_name:
    :type release_project_name: str
    :param release_definition:
    :type release_definition: str
    :param release_name:
    :type release_name: str
    :param release_env:
    :type release_env: str
    :param is_deployed:
    :type is_deployed: bool
    :param modified_on:
    :type modified_on: str
    """
    def __init__(self, release_project_name: str, release_definition: str, release_name: str, release_env: str, is_deployed: bool, modified_on: datetime):
        self.release_project_name = release_project_name
        self.release_definition = release_definition
        self.release_name = release_name
        self.release_env = release_env
        self.is_deployed = is_deployed
        self.modified_on = modified_on