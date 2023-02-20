from rest_framework import serializers

class ReleaseDetails(serializers.Serializer):
    project_name = serializers.CharField(max_length=200, required=True)
    release_name = serializers.CharField(max_length=200, required=True)
    target_number = serializers.IntegerField(min_value=0, required=True)
    rollback_number = serializers.IntegerField(min_value=0, required=True)
    
    def set_required_fields_for_via_latest(self):
        self.fields['target_number'].required = False
        self.fields['rollback_number'].required = False

class RunConfigurationsSerializer(serializers.Serializer):
    explicit_release_values = serializers.DictField()
    crucial_release_definitions = serializers.ListField(child = serializers.CharField(max_length=200))
    organization_url = serializers.CharField(max_length=200, required=True)
    personal_access_token = serializers.CharField(max_length=200, required=True)
    queries = serializers.ListField(child = serializers.CharField(max_length=200))
    release_name_format = serializers.CharField(max_length=200, required=True)
    release_target_env = serializers.CharField(max_length=200)
    search_only = serializers.BooleanField(required=True)
    via_env = serializers.BooleanField()
    via_env_source_name = serializers.CharField(max_length=200)
    via_env_latest_release = serializers.BooleanField()
    
    release_details = serializers.ListSerializer(child=ReleaseDetails())