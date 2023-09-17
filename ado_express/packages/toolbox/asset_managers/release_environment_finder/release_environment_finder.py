from ado_express.packages.authentication import MSAuthentication
from ado_express.packages.shared.environment_variables import \
    EnvironmentVariables
from ado_express.packages.shared.models import ReleaseEnvironment


class ReleaseEnvironmentFinder:

    def __init__(self, ms_authentication: MSAuthentication, environment_variables: EnvironmentVariables):
        self.release_client = ms_authentication.client
        self.release_client_v6 = ms_authentication.client_v6
        self.environment_variables = environment_variables

    def get_release_environment(self, deployment_detail, release_id):
        # Returns only the release env (aka stage) specified in deployment plan
        release_to_update_data = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release_id)

        for environment in release_to_update_data.environments:
            
            if str(environment.name).lower() == self.environment_variables.RELEASE_TARGET_ENV.lower():
                return ReleaseEnvironment(environment.name, environment.id, environment.status, environment)

    def get_release_environments(self, deployment_detail, release_id):
        # Returns all the release envs (aka stages)
        release_environments = [ReleaseEnvironment]
        release_to_update_data = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release_id)

        for environment in release_to_update_data.environments:
            release_environments.append(ReleaseEnvironment(environment.name, environment.id, environment.status, environment))
                
        return release_environments
    
    def get_release_environment_by_id(self, project, release_id, environment_id):
        release_environments = self.release_client_v6.get_release_environment(project, release_id, environment_id)

        return release_environments