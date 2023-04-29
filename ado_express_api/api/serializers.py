from base.models.ReleaseDetail import ReleaseDetail
from rest_framework import serializers


class DeploymentDetailSerializer(serializers.Serializer):
    releaseProjectName = serializers.CharField(max_length=200, required=True, source='release_project_name')
    releaseName = serializers.CharField(max_length=200, required=True, source='release_name')
    releaseNumber = serializers.IntegerField(min_value=0, required=False, allow_null=True, source='release_number')
    releaseRollback = serializers.IntegerField(min_value=0, required=False, allow_null=True, source='release_rollback')
    isCrucial = serializers.BooleanField(default=False, required=False, source='is_crucial')

    def set_required_fields_for_via_latest(self):
        self.fields['releaseNumber'].required = False
        self.fields['releaseRollback'].required = False

    def set_required_fields_for_via_number(self):
        self.fields['releaseRollback'].required = False

    def set_required_fields_for_via_environment(self):
        self.fields['releaseNumber'].required = False
        self.fields['releaseRollback'].required = False

class RunConfigurationSerializer(serializers.Serializer):
    explicitReleaseValues = serializers.DictField(allow_empty=True, allow_null=True, source='explicit_release_values')
    crucialReleaseDefinitions = serializers.ListField(child=serializers.CharField(max_length=200, allow_blank=True), allow_empty=True, allow_null=True, source='crucial_release_definitions')
    organizationUrl = serializers.CharField(max_length=200, required=True, source='organization_url')
    personalAccessToken = serializers.CharField(max_length=200, required=True, source='personal_access_token')
    queries = serializers.ListField(child=serializers.CharField(max_length=200), allow_empty=True, allow_null=True)
    releaseNameFormat = serializers.CharField(max_length=200, required=True, source='release_name_format')
    releaseTargetEnv = serializers.CharField(max_length=200, source='release_target_env')
    searchOnly = serializers.BooleanField(source='search_only')
    viaEnv = serializers.BooleanField(source='via_env')
    viaEnvSourceName = serializers.CharField(max_length=200, allow_null=True, allow_blank=True, required=False, source='via_env_source_name')
    viaEnvLatestRelease = serializers.BooleanField(source='via_env_latest_release')

    deploymentDetails = serializers.ListSerializer(child=DeploymentDetailSerializer(), allow_empty=True, allow_null=True, source='deployment_details')