import json

import status
from base.models.DeploymentDetails import DeploymentDetails
from base.models.ReleaseDetails import ReleaseDetails
from base.models.RunConfigurations import RunConfigurations
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ado_express.main import Startup

from .serializers import (DeploymentDetailsSerializer,
                          RunConfigurationsSerializer)


@api_view(['POST'])
def search_via_release_environment(request):
    deployment_details = DeploymentDetailsSerializer()
    deployment_details.set_required_fields_for_via_environment()

    serializer = RunConfigurationsSerializer(data=request.data)
    serializer.fields['deployment_details'].child = deployment_details

    # Fields required for via environment run
    serializer.fields['deployment_details'].allow_empty = False
    # Fields not required for via environment run
    serializer.fields['search_only'].required = False
    serializer.fields['via_env'].required = False
    serializer.fields['via_env_latest_release'].required = False

    if serializer.is_valid():
        run_configurations = RunConfigurations(serializer.validated_data['explicit_release_values'], 
                                               serializer.validated_data['crucial_release_definitions'], 
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               None,    # queries
                                               serializer.validated_data['release_name_format'], 
                                               serializer.validated_data['release_target_env'], 
                                               True,    # search_only
                                               True,    # via_env
                                               False,   # via_env_latest_release
                                               None,    #
                                               serializer.validated_data['deployment_details'])
        
        startup_runners = Startup(run_configurations)
        release_details = []

        #TODO Make concurrent
        for deployment in run_configurations.deployment_details:
            converted_deployment_details = DeploymentDetails(deployment['release_project_name'], deployment['release_name'], None, None, False)
            
            releases: list[ReleaseDetails] = startup_runners.search_and_log_details_only(converted_deployment_details)
            
            if releases: release_details.append(dict({'release_definition': deployment['release_name'], 'release_details': [release.__dict__ for release in releases]}))

        if release_details:
            return Response(status=status.HTTP_200_OK, data=release_details)
        else:
            return Response(status=status.HTTP_200_OK, data=[])
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Errors:\n{serializer.errors}")

@api_view(['POST'])
def search_via_latest_release(request):
    deployment_details = DeploymentDetailsSerializer()
    deployment_details.set_required_fields_for_via_latest()

    serializer = RunConfigurationsSerializer(data=request.data)
    serializer.fields['deployment_details'].child = deployment_details

    # Fields required for via latest run
    serializer.fields['deployment_details'].allow_empty = True
    serializer.fields['release_target_env'].required = True
    serializer.fields['via_env_source_name'].required = True
    # Fields not required for via latest run
    serializer.fields['search_only'].required = False
    serializer.fields['via_env'].required = False
    serializer.fields['via_env_latest_release'].required = False

    if serializer.is_valid():
        run_configurations = RunConfigurations(serializer.validated_data['explicit_release_values'], 
                                               serializer.validated_data['crucial_release_definitions'], 
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               serializer.validated_data['queries'], 
                                               serializer.validated_data['release_name_format'], 
                                               serializer.validated_data['release_target_env'],
                                               True,    # search_only
                                               True,    # via_env
                                               True,    # via_env_latest_release
                                               serializer.validated_data['via_env_source_name'],
                                               serializer.validated_data['deployment_details'])
        
        startup_runners = Startup(run_configurations)
        deployment_details = []

        #TODO Make concurrent
        for deployment in run_configurations.deployment_details:
            converted_deployment_details = DeploymentDetails(deployment['release_project_name'], deployment['release_name'], None, None, deployment['is_crucial'])
            
            release = startup_runners.get_deployment_detail_from_latest_release(converted_deployment_details)
            
            if release: deployment_details.append(release)

        if deployment_details:
            return Response(status=status.HTTP_200_OK, data={'releases': json.dumps([ob.__dict__ for ob in deployment_details])})
        else:
            return Response(status=status.HTTP_200_OK, data={'releases': []})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid.\n{serializer.error_messages}")
    
@api_view(['POST'])
def search_via_release_number(request):
    deployment_details = DeploymentDetailsSerializer()
    deployment_details.set_required_fields_for_via_number()

    serializer = RunConfigurationsSerializer(data=request.data)
    serializer.fields['deployment_details'].child = deployment_details

    # Fields required for via number run
    serializer.fields['deployment_details'].allow_empty = True
    # Fields not required for via number run
    serializer.fields['search_only'].required = False
    serializer.fields['via_env'].required = False
    serializer.fields['via_env_latest_release'].required = False
    serializer.fields['release_target_env'].allow_blank = True
    serializer.fields['via_env_source_name'].allow_blank = True
    print(serializer.initial_data)
    if not serializer.is_valid(): print(serializer.errors)

    if serializer.is_valid():
        run_configurations = RunConfigurations(None, # explicit_release_values
                                               None, # crucial_release_definitions
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               None,    # queries
                                               serializer.validated_data['release_name_format'], 
                                               None,    # release_target_env
                                               True,    # search_only
                                               False,   # via_env
                                               False,   # via_env_latest_release
                                               None,    # via_env_source_name
                                               serializer.validated_data['deployment_details'])
        
        startup_runners = Startup(run_configurations)
        release_details = []
        
        #TODO Make concurrent
        for deployment in run_configurations.deployment_details:
            converted_deployment_details = DeploymentDetails(deployment['release_project_name'], deployment['release_name'], deployment['release_number'], None, deployment['is_crucial'])
            
            releases: list[ReleaseDetails] = startup_runners.search_and_log_details_only(converted_deployment_details)
            
            if releases: release_details.append(dict({'release_definition': deployment['release_name'], 'release_name': deployment['release_number'], 'results': [release.__dict__ for release in releases]}))
        
        if release_details:
            return Response(status=status.HTTP_200_OK, data={'releases': json.dumps(release_details, default=str)})
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
    # Fields not required for query run
    serializer.fields['search_only'].required = False

    if serializer.is_valid():
        run_configurations = RunConfigurations(serializer.validated_data['explicit_release_values'], 
                                               serializer.validated_data['crucial_release_definitions'], 
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               serializer.validated_data['queries'], 
                                               serializer.validated_data['release_name_format'], 
                                               serializer.validated_data['release_target_env'], 
                                               True,    # search_only
                                               serializer.validated_data['via_env'], 
                                               serializer.validated_data['via_env_latest_release'],
                                               serializer.validated_data['via_env_source_name'],
                                               serializer.validated_data['deployment_details'])
        
        startup_runners = Startup(run_configurations)
        deployment_details = startup_runners.get_deployment_details_from_query()

        if deployment_details:
            return Response(status=status.HTTP_200_OK, data={'releases': json.dumps([ob.__dict__ for ob in deployment_details])})
        else:
            return Response(status=status.HTTP_200_OK, data={'releases': []})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid.\n{serializer.error_messages}")
