import concurrent.futures
from itertools import repeat
import logging

from packages.authentication import MSAuthentication
from packages.common.constants import Constants
from packages.common.enums import ReleaseEnvironmentStatuses
from packages.common.environment_variables import EnvironmentVariables
from packages.common.models import DeploymentDetails

class ReleaseFinder:

    def __init__(self, ms_authentication: MSAuthentication, environment_variables: EnvironmentVariables):
        self.work_client = ms_authentication.work_client
        self.build_client = ms_authentication.build_client
        self.release_client = ms_authentication.client
        self.release_client_v6 = ms_authentication.client_v6
        self.environment_variables = environment_variables
        self.environment_statuses = ReleaseEnvironmentStatuses()

    def find_matching_release_via_name(self, releases, release_number):
        for release in releases:
            
            if str(release.name).lower() == (self.environment_variables.RELEASE_NAME_FORMAT.split('$')[0].lower() + str(release_number)):
                return release

    def find_matching_releases_via_name(self, releases, release_number, deployment_detail: DeploymentDetails):
        found = False

        for release in releases:
            
            if str(release.name).lower() == (self.environment_variables.RELEASE_NAME_FORMAT.split('$')[0].lower() + str(release_number)):
                release_to_check = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release.id)

                for env in release_to_check.environments:
                    logging.info(f"Release Definition: {deployment_detail.release_name}\t Release: {release_to_check.name}\t Stage: {env.name}\t Status: {env.status}\t Modified On: {env.modified_on}\n")            
                    found = True
                
        if not found: logging.info(f"\nNO RESULTS AVAILABLE - Release Definition: {deployment_detail.release_name}\n")
                
    def find_matching_release_via_source_stage(self, releases, deployment_detail, rollback=False):
        environment_name_to_find = self.environment_variables.RELEASE_TARGET_ENV if rollback else self.environment_variables.VIA_ENV_SOURCE_NAME
        is_query_call = True if isinstance(deployment_detail, str) else False
        # If deployment details are coming from query dict they will be str
        project = deployment_detail.split('/')[0] if is_query_call else deployment_detail.release_project_name 
        
        for release in releases:
            release_to_check = self.release_client.get_release(project, release_id=release.id)

            for env in release_to_check.environments:
                
                if str(env.name).lower() == environment_name_to_find and env.status in self.environment_statuses.Succeeded:
                    
                    if is_query_call: return {deployment_detail: release.name}
                    else: return release
            
        return {deployment_detail: None} # If no matching release was found


    def find_matching_releases_via_env(self, releases, deployment_detail: DeploymentDetails):
        found = False
        
        for release in releases:
            release_to_check = self.release_client.get_release(project=deployment_detail.release_project_name, release_id=release.id)

            for env in release_to_check.environments:

                if str(env.name).lower() == self.environment_variables.RELEASE_TARGET_ENV and env.status in self.environment_statuses.Succeeded:
                    logging.info(f"Release Definition: {deployment_detail.release_name}\t Release: {release_to_check.name}\t Stage: {env.name}\t Status: {env.status}\t Modified On: {env.modified_on}\n")          
                    found = True
                    
        if not found: logging.info(f'\nNO RESULTS AVAILABLE - Release Definition: {deployment_detail.release_name}\n')

    def get_release(self, deployment_detail, find_via_env=False, rollback=False, via_latest=False):
        # If deployment details are coming from query dict they will be str
        project = deployment_detail.split('/')[0] if isinstance(deployment_detail, str) else deployment_detail.release_project_name 
        release_name = deployment_detail.split('/')[1] if isinstance(deployment_detail, str) else deployment_detail.release_name
        # Gets release definitions names 
        release_definitions = self.release_client.get_release_definitions(project)
        
        for definition in release_definitions.value:
            
            if (str(definition.name).lower() == str(release_name).lower()):
                release_definition = definition

        # Get release id from release to know which needs to be deployed to new env
        releases = self.release_client.get_releases(project, definition_id=release_definition.id).value
        
        if find_via_env and via_latest or rollback:
            return self.find_matching_release_via_source_stage(releases, deployment_detail, rollback) 
        else:
            if rollback:
                release_number = deployment_detail.release_rollback
            else: 
                release_number = deployment_detail.release_number

            return self.find_matching_release_via_name(releases, release_number)

    def get_releases(self, deployment_detail, find_via_env=False, rollback=False):
        # Gets release definitions names 
        release_definitions = self.release_client.get_release_definitions(project=deployment_detail.release_project_name)
        
        for definition in release_definitions.value:
            
            if (str(definition.name).lower() == str(deployment_detail.release_name).lower()):
                release_definition = definition

        # Get release id from release to know which needs to be deployed to new env
        releases = self.release_client.get_releases(project=deployment_detail.release_project_name, definition_id=release_definition.id).value
        
        if find_via_env:
            return self.find_matching_releases_via_env(releases, deployment_detail) 
        else:
            if not rollback:
                release_number = deployment_detail.release_number
            else: 
                release_number = deployment_detail.release_rollback
                
            self.find_matching_releases_via_name(releases, release_number, deployment_detail)

    def get_releases_dict_from_build_releases(self, release, release_name_split_key):
        environment_name_to_find = self.environment_variables.VIA_ENV_SOURCE_NAME
        releases_dict = dict()
        release_project = release.project_reference.name
        release_definition = release.release_definition
        release_definition_name = release_definition.name
        dict_key = f'{release_project}/{release_definition_name}'

        if dict_key in releases_dict:
        
            if release.name.split(release_name_split_key)[-1] > releases_dict[dict_key].split(release_name_split_key)[-1]: 

                if environment_name_to_find is None: releases_dict[dict_key] = release.name
                else:
                    release_to_add = self.release_client.get_release(project=release_project, release_id=release.id)
                    
                    for env in release_to_add.environments:
                        if str(env.name).lower() == environment_name_to_find and env.status in self.environment_statuses.Succeeded: releases_dict[dict_key] = release.name
        else: 
            if environment_name_to_find is None: releases_dict[dict_key] = release.name
            else:
                release_to_add = self.release_client.get_release(project=release_project, release_id=release.id)
                
                for env in release_to_add.environments:
                    if str(env.name).lower() == environment_name_to_find and env.status in self.environment_statuses.Succeeded: releases_dict[dict_key] = release.name
        
        return releases_dict
    
    def get_releases_from_build_id(self, build_id):
        release = self.release_client.get_releases(artifact_version_id=build_id).value
        project = None
        description = None

        for release_details in release: 
            description = release_details.description
            project = release_details.project_reference.name

        if project and description: 
            build = self.build_client.get_build(project, build_id)
            # Ensure build was the trigger of release
            if build.definition.name in description:
                return release
        
        return None
    
    def get_releases_via_builds(self, build_ids, release_name_split_key='Release-'):
        releases_dict = dict()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            releases = []
            build_releases = executor.map(self.get_releases_from_build_id, build_ids)
            # TODO: Refactor this
            for release in build_releases:
                if release is not None:
                    releases.append(release)
            releases_dicts = executor.map(self.get_releases_dict_from_build_releases, [item for sublist in releases for item in sublist if build_releases is not None], repeat(release_name_split_key))
            
            for release_dictionary in releases_dicts:

                for release_definition, release_name in release_dictionary.items():

                    if release_definition in releases_dict:
                        if release_name.split(release_name_split_key)[-1] > releases_dict[release_definition].split(release_name_split_key)[-1]: releases_dict[release_definition] = release_name
                    else: 
                        releases_dict[release_definition] = release_name
        
        return releases_dict