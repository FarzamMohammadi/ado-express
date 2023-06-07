from rest_framework import serializers


class DeploymentDetailSerializer(serializers.Serializer):
    releaseProjectName = serializers.CharField(max_length=200, required=True, source='release_project_name')
    releaseName = serializers.CharField(max_length=200, required=True, source='release_name')
    releaseNumber = serializers.IntegerField(min_value=0, required=False, allow_null=True, source='release_number')
    releaseRollback = serializers.IntegerField(min_value=0, required=False, allow_null=True, source='release_rollback')
    isCrucial = serializers.BooleanField(default=False, required=False, source='is_crucial')


class RunConfigurationSerializer(serializers.Serializer):
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

    def set_field_requirements_for_via_latest(self):
        # Fields required for via latest run
        self.fields['deploymentDetails'].allow_empty = True
        self.fields['releaseTargetEnv'].required = True
        self.fields['viaEnvSourceName'].required = True
        # Fields not required for via latest run
        self.fields['searchOnly'].required = False
        self.fields['viaEnv'].required = False
        self.fields['viaEnvLatestRelease'].required = False

    def set_field_requirements_for_via_number(self):
        # Fields required for via number run
        self.fields['deploymentDetails'].allow_empty = True
        # Fields not required for via number run
        self.fields['searchOnly'].required = False
        self.fields['viaEnv'].required = False
        self.fields['viaEnvLatestRelease'].required = False
        self.fields['releaseTargetEnv'].allow_blank = True
        self.fields['viaEnvSourceName'].allow_blank = True

    def set_field_requirements_for_via_environment(self):
        # Fields required for via environment run
        self.fields['deploymentDetails'].allow_empty = False
        # Fields not required for via environment run
        self.fields['searchOnly'].required = False
        self.fields['viaEnv'].required = False
        self.fields['viaEnvLatestRelease'].required = False

    def set_field_requirements_for_via_query(self):
        # Fields required for query run
        self.fields['queries'].required = True
        self.fields['releaseTargetEnv'].required = True
        self.fields['viaEnv'].required = True
        # Fields not required for query run
        self.fields['searchOnly'].required = False


class DeploymentStatusSerializer:
    def __init__(self, comment: str, percentage: int, status: str):
        self.comment = comment
        self.percentage = percentage
        self.status = status

    def to_dict(self):
        return {
            'comment': self.comment,
            'percentage': self.percentage,
            'status': self.status,
        }


class ReleaseDeploymentStatus(serializers.Serializer):
    comment = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    percentage = serializers.IntegerField(min_value=0, max_value=100, required=True)
    status = serializers.CharField(max_length=200, required=True)

    def create(self, validated_data):
        return DeploymentStatusSerializer(**validated_data)


class GenericWebsocketMessageSerializer:
    def __init__(self, message: str, show_idle_dots: bool = False):
        self.message = message
        self.show_idle_dots = show_idle_dots

    def to_dict(self):
        return {
            'message': self.message,
            'showIdleDots': self.show_idle_dots,
        }


class GenericWebsocketMessage:
    message = serializers.CharField()
    show_idle_dots = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return GenericWebsocketMessageSerializer(**validated_data)
