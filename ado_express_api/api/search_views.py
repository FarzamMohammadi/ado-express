import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

from base.models.RunConfigurations import RunConfigurations
from base.models.ReleaseDetails import ReleaseDetails
from .serializers import RunConfigurationsSerializer, ReleaseDetailsSerializer
import status
from ado_express.main import Startup

@api_view(['POST'])
def search_via_latest_release(request):
    release_details = ReleaseDetailsSerializer()
    # Fields not required for via latest run
    release_details.set_required_fields_for_via_latest()

    serializer = RunConfigurationsSerializer(data=request.data)
    serializer.fields['release_details'].child = release_details

    # Fields required for via latest run
    serializer.fields['release_details'].required = True
    serializer.fields['release_target_env'].required = True
    serializer.fields['via_env_source_name'].required = True
    print(serializer.initial_data)
    if serializer.is_valid():
        run_configurations = RunConfigurations(serializer.validated_data['explicit_release_values'], 
                                               serializer.validated_data['crucial_release_definitions'], 
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               serializer.validated_data['queries'], 
                                               serializer.validated_data['release_name_format'], 
                                               serializer.validated_data['release_target_env'],
                                               True, # search_only
                                               True, # via_env
                                               True, # via_env_latest_release
                                               serializer.validated_data['via_env_source_name'],
                                               serializer.validated_data['release_details'])
        
        startup_runners = Startup(run_configurations)
        deployment_details = []

        #TODO Make async
        for release_details in run_configurations.release_details:
            converted_release_details = ReleaseDetails(release_details['release_project_name'], release_details['release_name'], None, None, release_details['is_crucial'])
            
            release = startup_runners.get_deployment_detail_from_latest_release(converted_release_details)
            
            if release: deployment_details.append(release)

        if deployment_details:
            return Response(status=status.HTTP_200_OK, data={'releases': json.dumps([ob.__dict__ for ob in deployment_details])})
        else:
            return Response(status=status.HTTP_200_OK, data={'releases': []})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid.\n{serializer.error_messages}")


@api_view(['POST'])
def search_via_query(request):
    serializer = RunConfigurationsSerializer(data=request.data)
    # Fields required for query run
    serializer.fields['queries'].required = True
    serializer.fields['release_target_env'].required = True
    serializer.fields['via_env'].required = True

    if serializer.is_valid():
        run_configurations = RunConfigurations(serializer.validated_data['explicit_release_values'], 
                                               serializer.validated_data['crucial_release_definitions'], 
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               serializer.validated_data['queries'], 
                                               serializer.validated_data['release_name_format'], 
                                               serializer.validated_data['release_target_env'], 
                                               True, # search_only
                                               serializer.validated_data['via_env'], 
                                               serializer.validated_data['via_env_latest_release'],
                                               serializer.validated_data['via_env_source_name'],
                                               serializer.validated_data['release_details'])
        
        startup_runners = Startup(run_configurations)
        deployment_details = startup_runners.get_deployment_details_from_query()

        return Response(status=status.HTTP_200_OK, data={'releases': json.dumps([ob.__dict__ for ob in deployment_details])})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid.\n{serializer.error_messages}")
