from rest_framework import serializers

class ReleaseDetailsSerializer(serializers.Serializer):
    release_project_name = serializers.CharField(max_length=200, required=True)
    release_name = serializers.CharField(max_length=200, required=True)
    release_number = serializers.IntegerField(min_value=0, required=True)
    release_rollback = serializers.IntegerField(min_value=0, required=True)
    is_crucial = serializers.BooleanField(default=False)
    
    def set_required_fields_for_via_latest(self):
        self.fields['release_number'].required = False
        self.fields['release_rollback'].required = False

    def set_required_fields_for_via_number(self):
        self.fields['release_rollback'].required = False

class RunConfigurationsSerializer(serializers.Serializer):
    explicit_release_values = serializers.DictField()
    crucial_release_definitions = serializers.ListField(child = serializers.CharField(max_length=200))
    organization_url = serializers.CharField(max_length=200, required=True)
    personal_access_token = serializers.CharField(max_length=200, required=True)
    queries = serializers.ListField(child = serializers.CharField(max_length=200))
    release_name_format = serializers.CharField(max_length=200, required=True)
    release_target_env = serializers.CharField(max_length=200)
    search_only = serializers.BooleanField()
    via_env = serializers.BooleanField()
    via_env_source_name = serializers.CharField(max_length=200)
    via_env_latest_release = serializers.BooleanField()
    
    release_details = serializers.ListSerializer(child=ReleaseDetailsSerializer())