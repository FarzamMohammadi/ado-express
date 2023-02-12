

class RunConfigurations():

    def __init__(self, crucial_release_definitions: list[str], organization_url: str, personal_access_token: str, queries: list[str], release_name_format: str, release_target_env: str, search_only: bool, via_env: bool, via_env_source_name: str, via_env_latest_release: bool):
        self.crucial_release_definitions = crucial_release_definitions
        self.organization_url = organization_url
        self.personal_access_token = personal_access_token
        self.queries = queries
        self.release_name_format = release_name_format
        self.release_target_env = release_target_env
        self.search_only = search_only
        self.via_env = via_env
        self.via_env_source_name = via_env_source_name
        self.via_env_latest_release = via_env_latest_release

    # @staticmethod
    # def from_json(json_dict):
    #   return RunConfigurations(json_dict['crucial_release_definitions'], json_dict['organization_url'], json_dict['personal_access_token'], json_dict['queries'], json_dict['release_name_format'], json_dict['release_target_env'], json_dict['search_only'], json_dict['via_env'], json_dict['via_env_source_name'], json_dict['via_env_latest_release'])