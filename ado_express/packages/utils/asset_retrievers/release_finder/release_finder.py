from packages.authentication import MSAuthentication
from packages.common.constants import Constants
from packages.common.enums import ReleaseEnvironmentStatuses
from packages.common.environment_variables import EnvironmentVariables
from packages.common.models import DeploymentDetails

class ReleaseFinder:

    def __init__(self, ms_authentication: MSAuthentication, deployment_details: list[DeploymentDetails], environment_variables: EnvironmentVariables):
        self.release_client = ms_authentication.client
        self.release_client_v6 = ms_authentication.client_v6
        self.deployment_details = deployment_details
        self.environment_variables = environment_variables
        self.environment_statuses = ReleaseEnvironmentStatuses()

    def find_matching_release_via_name(self, releases, release_number):
        for release in releases:
            
            if str(release.name).lower() == (self.environment_variables.RELEASE_NAME_FORMAT.split('$')[0].lower() + str(release_number)):
                return release

    def find_matching_releases_via_name(self, releases, release_number, deployment_detail: DeploymentDetails):
        constants = Constants()

        for release in releases:

            if str(release.name).lower() == (self.environment_variables.RELEASE_NAME_FORMAT.split('$')[0].lower() + str(release_number)):
                release_to_check = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release.id)

                for env in release_to_check.environments:
                    with open(constants.SEARCH_RESULTS_FILE_PATH, "a") as file:
                        file.write(f"Release Definition: {deployment_detail.release_name}\t Release: {release_to_check.name}\t Stage: {env.name}\t Status: {env.status}\t Modified On: {env.modified_on}\n")            

    def find_matching_release_via_source_stage(self, releases, deployment_detail: DeploymentDetails, rollback=False):
        environment_name_to_find = self.environment_variables.RELEASE_STAGE_NAME if rollback else self.environment_variables.VIA_STAGE_SOURCE_NAME
        
        for release in releases:
            release_to_check = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release.id)

            for env in release_to_check.environments:
                if str(env.name).lower() == environment_name_to_find and env.status in self.environment_statuses.Succeeded:
                    return release


    def find_matching_releases_via_stage(self, releases, deployment_detail: DeploymentDetails):
        constants = Constants()

        for release in releases:
            release_to_check = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release.id)

            for env in release_to_check.environments:
                
                if str(env.name).lower() == self.environment_variables.RELEASE_STAGE_NAME and env.status in self.environment_statuses .Succeeded:
                    with open(constants.SEARCH_RESULTS_FILE_PATH, "a") as file:
                        file.write(f"Release Definition: {deployment_detail.release_name}\t Release: {release_to_check.name}\t Stage: {env.name}\t Status: {env.status}\t Modified On: {env.modified_on}\n")            


    def get_release(self, deployment_detail, find_via_stage=False, rollback=False):
        # Gets release definitions names 
        release_definitions = self.release_client.get_release_definitions(project=deployment_detail.release_project_name)
        
        for definition in release_definitions.value:
            
            if (str(definition.name).lower() == str(deployment_detail.release_name).lower()):
                release_definition = definition

        # Get release id from release to know which needs to be deployed to new env
        releases = self.release_client.get_releases(project=deployment_detail.release_project_name, definition_id=release_definition.id).value
        
        if find_via_stage:
            return self.find_matching_release_via_source_stage(releases, deployment_detail, rollback) 
        else:
            if rollback:
                release_number = deployment_detail.release_rollback
            else: 
                release_number = deployment_detail.release_number

            return self.find_matching_release_via_name(releases, release_number)

    def get_releases(self, deployment_detail, find_via_stage=False, rollback=False):
        # Gets release definitions names 
        release_definitions = self.release_client.get_release_definitions(project=deployment_detail.release_project_name)
        
        for definition in release_definitions.value:
            
            if (str(definition.name).lower() == str(deployment_detail.release_name).lower()):
                release_definition = definition

        # Get release id from release to know which needs to be deployed to new env
        releases = self.release_client.get_releases(project=deployment_detail.release_project_name, definition_id=release_definition.id).value
        
        if find_via_stage:
            self.find_matching_releases_via_stage(releases, deployment_detail) 
        else:
            if not rollback:
                release_number = deployment_detail.release_number
            else: 
                release_number = deployment_detail.release_rollback
                
            self.find_matching_releases_via_name(releases, release_number, deployment_detail)