from .DeploymentDetail import DeploymentDetail


class RunConfiguration:
  """
  :param explicit_release_values:
  :type EXPLICIT_RELEASE_VALUES: dict
  :param crucial_release_definitions:
  :type CRUCIAL_RELEASE_DEFINITIONS: list[str]
  :param organization_url:
  :type ORGANIZATION_URL: str
  :param personal_access_token:
  :type PERSONAL_ACCESS_TOKEN: str
  :param queries:
  :type QUERIES: list[str]
  :param release_name_format:
  :type RELEASE_NAME_FORMAT: str
  :param release_target_env:
  :type RELEASE_TARGET_ENV: str
  :param search_only:
  :type SEARCH_ONLY: bool
  :param via_env:
  :type VIA_ENV: bool
  :param via_env_latest_release:
  :type VIA_ENV_LATEST_RELEASE: bool
  :param via_env_source_name:
  :type VIA_ENV_SOURCE_NAME: str
  :param deployment_details:
  :type deployment_details: list[DeploymentDetail]
  """
  def __init__(self, explicit_release_values: dict, crucial_release_definitions: list[str], organization_url: str, personal_access_token: str, queries: list[str], release_name_format: str, release_target_env: str, search_only: bool, via_env: bool, via_env_latest_release: bool, via_env_source_name: str, deployment_details: list[DeploymentDetail]):
    self.EXPLICIT_RELEASE_VALUES = explicit_release_values
    self.CRUCIAL_RELEASE_DEFINITIONS = crucial_release_definitions
    self.ORGANIZATION_URL = organization_url
    self.PERSONAL_ACCESS_TOKEN = personal_access_token
    self.QUERIES = queries
    self.RELEASE_NAME_FORMAT = release_name_format
    self.RELEASE_TARGET_ENV = release_target_env
    self.SEARCH_ONLY = search_only
    self.VIA_ENV = via_env
    self.VIA_ENV_LATEST_RELEASE = via_env_latest_release
    self.VIA_ENV_SOURCE_NAME = via_env_source_name
    self.deployment_details = deployment_details

  # Used mainly for testing to reverse map values for an api call
  def to_dict_with_lowercase_keys(self):
    deployment_details_dicts = []

    if self.deployment_details: 
      for deployment in self.deployment_details:
        deployment_details_dicts.append(deployment.__dict__)

    lowered_dict_values = {k.lower(): v for k, v in self.__dict__.items()} 
    lowered_dict_values['deployment_details'] = deployment_details_dicts
    
    return lowered_dict_values

  