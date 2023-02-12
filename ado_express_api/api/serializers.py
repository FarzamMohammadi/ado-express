from rest_framework import serializers

class RunConfigurationsSerializer(serializers.Serializer):
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