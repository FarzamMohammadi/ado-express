import json
import time
from threading import Thread

import status
from base.models.DeploymentDetail import DeploymentDetail
from base.models.RunConfiguration import RunConfiguration
from rest_framework.decorators import api_view
from rest_framework.response import Response
from websocket_server.consumers import WebSocketConsumer

from ado_express.main import Startup
from ado_express.packages.common.models.deployment_status import \
    DeploymentStatus

from .serializers import (DeploymentDetailSerializer,
                          DeploymentStatusSerializer,
                          RunConfigurationSerializer)


# -Deployment via number-
# This method does not run a search 
# Deployment details must be provided in the request body
# If a search is required, it must be done beforehand
@api_view(['POST'])
def deploy(request):
    deployment_details_serializer = DeploymentDetailSerializer()
    serializer = RunConfigurationSerializer(data=request.data)

    serializer.fields['deploymentDetails'].child = deployment_details_serializer

    # Fields required for run
    serializer.fields['deploymentDetails'].allow_empty = False
    
    if serializer.is_valid():
        run_configurations = RunConfiguration(serializer.validated_data['explicit_release_values'], 
                                               serializer.validated_data['crucial_release_definitions'], 
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               serializer.validated_data['queries'], 
                                               serializer.validated_data['release_name_format'], 
                                               serializer.validated_data['release_target_env'], 
                                               False,    # search_only
                                               serializer.validated_data['via_env'], 
                                               serializer.validated_data['via_env_latest_release'],
                                               serializer.validated_data['via_env_source_name'],
                                               serializer.validated_data['deployment_details'])
        
        ado_express = Startup(run_configurations)
        deployment_details = []
        
        for deployment in run_configurations.deployment_details:
            converted_deployment_details = DeploymentDetail(deployment['release_project_name'], deployment['release_name'], deployment['release_number'], deployment['release_rollback'], deployment['is_crucial'])
            deployment_details.append(converted_deployment_details)
        
        explicit_deployment_details = ado_express.updated_deployment_details_based_on_explicit_inclusion_and_exclusion(deployment_details)
        if explicit_deployment_details: deployment_details = explicit_deployment_details
        
        crucial_deployment_details = []
        # Needs to be null so get_crucial_release_definitions knows to check deployment_details instead
        if run_configurations.CRUCIAL_RELEASE_DEFINITIONS == []: run_configurations.CRUCIAL_RELEASE_DEFINITIONS = None
        
        crucial_release_definitions = ado_express.get_crucial_release_definitions(deployment_details)
        
        if crucial_release_definitions:
            # Separate crucial & regular deployments based on release definitions that match CRUCIAL_RELEASE_DEFINITIONS env variable list
            crucial_deployment_details = ado_express.get_crucial_deployment_from_deployment_details(deployment_details, crucial_release_definitions)
            deployment_details[:] = ado_express.remove_crucial_deployments_from_deployment_details(deployment_details, crucial_release_definitions)

        def run_deployments_in_background():
            has_crucial_deployments = False

            if crucial_deployment_details:
                ado_express.run_release_deployments(crucial_deployment_details, True)
                process_deployments(crucial_deployment_details, ado_express)

                has_crucial_deployments = True

            if deployment_details:
                ado_express.run_release_deployments(deployment_details, False, has_crucial_deployments)
                process_deployments(deployment_details, ado_express)

        # Start a new thread to run the deployments in the background
        deployment_thread = Thread(target=run_deployments_in_background)
        deployment_thread.start()

        return Response(status=status.HTTP_200_OK, data={})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"\n{serializer.errors}")
    
def process_deployments(deployment_details, ado_express: Startup):
    deployments_complete = False
    completed_deployments = []

    while not deployments_complete:
        for deployment_detail in deployment_details:
            if deployment_detail.release_name not in completed_deployments:
                deployment_is_complete = ado_express.release_deployment_completed(deployment_detail)

                if deployment_is_complete:
                    completed_deployments.append(deployment_detail.release_name)

                latest_deployment_status: DeploymentStatus = ado_express.get_deployment_status(deployment_detail)
                
                if latest_deployment_status is None: 
                    deployment_status = dict()
                    deployment_status[deployment_detail.release_name] = DeploymentStatusSerializer('Unable to retrieve deployment status - Please check ADO', 0, 'Unknown')
                    
                    WebSocketConsumer.send_message(json.dumps({key: value.to_dict() for key, value in deployment_status.items()}))
                    
                    completed_deployments.append(deployment_detail.release_name) 
                    continue

                deployment_status = dict()
                deployment_status[deployment_detail.release_name] = DeploymentStatusSerializer(latest_deployment_status.comment, latest_deployment_status.percentage, latest_deployment_status.status)

                WebSocketConsumer.send_message(json.dumps({key: value.to_dict() for key, value in deployment_status.items()}))

                if not deployment_is_complete:
                    time.sleep(1)

        if len(completed_deployments) == len(deployment_details):
            deployments_complete = True

    return deployments_complete