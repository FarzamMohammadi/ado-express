# from django.db import models
# from django.contrib.postgres.fields import ArrayField

# Create your models here.

# class RunErrors(models.Model):
#     title = models.CharField(max_length=200)
#     code = models.CharField(max_length=3)
#     message = models.TextField()

# class RunConfigurations():

#     def __init__(self, crucial_release_definitions: List[str], organization_url: str, target: str, personal_access_token: str, queries: List[str], release_name_format: str, release_target_env: str, search_only: bool, via_env: bool, via_env_source_name: str, via_env_latest_release: bool):
#         self.crucial_release_definitions = crucial_release_definitions
#         self.organization_url = organization_url
#         self.personal_access_token = personal_access_token
#         self.queries = queries
#         self.release_name_format = release_name_format
#         self.release_target_env = release_target_env
#         self.search_only = search_only
#         self.via_env = via_env
#         self.via_env_source_name = via_env_source_name
#         self.via_env_latest_release = via_env_latest_release
    

# class DeploymentDetails():

#     def __init__(self, project: str, definition: str, target: int, rollback: int):
#         self.project = project
#         self.definition = definition
#         self.target = target
#         self.rollback = rollback

# class SearchResults():

#     def init(self, deployments: List[DeploymentDetails]):
#         self.deployments: deployments


# class RunConfigurations(models.Model):

#     crucial_release_definitions = ArrayField(models.CharField(max_length=200))
#     organization_url = models.CharField(max_length=200)
#     personal_access_token = models.CharField(max_length=200)
#     queries = ArrayField(models.CharField(max_length=200))
#     release_name_format = models.CharField(max_length=200)
#     release_target_env = models.CharField(max_length=200)
#     search_only = models.BooleanField()
#     via_env = models.BooleanField()
#     via_env_source_name = models.CharField(max_length=200)
#     via_env_latest_release = models.BooleanField()