import json
import time
from threading import Thread

import status
from base.models.DeploymentDetail import DeploymentDetail
from base.models.enums.WebsocketMessageType import WebsocketMessageType
from base.models.RunConfiguration import RunConfiguration
from rest_framework.decorators import api_view
from rest_framework.response import Response
from websocket_server.consumers import WebSocketConsumer

from ado_express.main import ADOExpress
from ado_express.packages.shared.models.deployment_status import \
    DeploymentStatus
from ado_express_api.base.models.enums.DeploymentStatusLabel import \
    DeploymentStatusLabel

from .serializers import (DeploymentDetailSerializer,
                          DeploymentStatusSerializer,
                          GenericWebsocketMessageSerializer,
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
        run_configurations = RunConfiguration(
            None,
            None,
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

        ado_express = ADOExpress(run_configurations)
        deployment_details = []

        for deployment in run_configurations.deployment_details:
            converted_deployment_details = DeploymentDetail(
                deployment['release_project_name'], deployment['release_name'], deployment['release_number'], deployment['release_rollback'], deployment['is_crucial'])
            deployment_details.append(converted_deployment_details)

        crucial_deployment_details = []
        # Needs to be null so get_crucial_release_definitions knows to check deployment_details instead
        if run_configurations.CRUCIAL_RELEASE_DEFINITIONS == []:
            run_configurations.CRUCIAL_RELEASE_DEFINITIONS = None

        crucial_release_definitions = ado_express.get_crucial_release_definitions(
            deployment_details)

        if crucial_release_definitions:
            # Separate crucial & regular deployments based on release definitions that match CRUCIAL_RELEASE_DEFINITIONS env variable list
            crucial_deployment_details = ado_express.get_crucial_deployment_from_deployment_details(
                deployment_details, crucial_release_definitions)
            deployment_details[:] = ado_express.remove_crucial_deployments_from_deployment_details(
                deployment_details, crucial_release_definitions)

        def run_deployments_in_background():
            had_crucial_deployments = False

            if crucial_deployment_details:
                message = GenericWebsocketMessageSerializer(
                    '\nDeploying crucial releases', True)
                WebSocketConsumer.send_message(json.dumps(
                    message.to_dict()), WebsocketMessageType.Generic.value)

                ado_express.run_release_deployments(
                    crucial_deployment_details, True)

                failed_deployment_details = send_live_status_data_and_check_for_failures(
                    crucial_deployment_details, ado_express)

                if failed_deployment_details.__len__() > 0:
                    ado_express.run_release_deployments(
                        failed_deployment_details, True, True)

                    message = GenericWebsocketMessageSerializer(
                        'Crucial release deployment(s) failed. Stopping deployment process and rolling back the failed deployment(s).', False)
                    WebSocketConsumer.send_message(json.dumps(
                        message.to_dict()), WebsocketMessageType.Generic.value)

                    send_live_status_data_and_check_for_failures(
                        failed_deployment_details, ado_express, True)

                    return

                had_crucial_deployments = True

                message = GenericWebsocketMessageSerializer(
                    'Crucial release deployments are now complete.')
                WebSocketConsumer.send_message(json.dumps(
                    message.to_dict()), WebsocketMessageType.Generic.value)

            if deployment_details:

                if had_crucial_deployments:
                    message = GenericWebsocketMessageSerializer(
                        '\nNow, deploying the rest of the releases', True)
                    WebSocketConsumer.send_message(json.dumps(
                        message.to_dict()), WebsocketMessageType.Generic.value)
                else:
                    message = GenericWebsocketMessageSerializer(
                        '\nDeploying releases', True)
                    WebSocketConsumer.send_message(json.dumps(
                        message.to_dict()), WebsocketMessageType.Generic.value)

                ado_express.run_release_deployments(
                    deployment_details, False, False, had_crucial_deployments)
                
                failed_deployment_details = send_live_status_data_and_check_for_failures(
                    deployment_details, ado_express)

                if failed_deployment_details.__len__() > 0:
                    ado_express.run_release_deployments(
                        failed_deployment_details, True, True)

                    message = GenericWebsocketMessageSerializer(
                        'Release deployment(s) failed. Rolling back the failed deployment(s).', False)
                    WebSocketConsumer.send_message(json.dumps(
                        message.to_dict()), WebsocketMessageType.Generic.value)

                    send_live_status_data_and_check_for_failures(
                        failed_deployment_details, ado_express, True)

                    return

                message = GenericWebsocketMessageSerializer(
                    '\nAll release deployments are now complete. Have a great day!', False)
                WebSocketConsumer.send_message(json.dumps(
                    message.to_dict()), WebsocketMessageType.Generic.value)

        # Start a new thread to run the deployments in the background
        deployment_thread = Thread(target=run_deployments_in_background)
        deployment_thread.start()

        return Response(status=status.HTTP_200_OK, data={})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"\n{serializer.errors}")


def construct_and_send_deployment_status(deployment_detail, latest_deployment_status, rollback):
    deployment_status = dict()

    if rollback:
        if latest_deployment_status.status == DeploymentStatusLabel.failed.value:
            status = 'Rollback Failed'
        elif latest_deployment_status.status == DeploymentStatusLabel.succeeded.value:
            status = 'Rollback Succeeded'
        else:
            status = 'Rollback In Progress'
    else:
        status = latest_deployment_status.status

    deployment_status[deployment_detail.release_name] = DeploymentStatusSerializer(latest_deployment_status.comment, latest_deployment_status.percentage, status)
    WebSocketConsumer.send_message(json.dumps({key: value.to_dict() for key, value in deployment_status.items()}), WebsocketMessageType.DeploymentStatus.value)


def handle_deployment_and_send_status(ado_express, deployment_detail, deployment_details, rollback, failed_deployment_details):
    completed_deployments = []
    deployment_is_complete = False

    while deployment_detail.release_name not in completed_deployments:
        completed_deployments, failed_deployment_details, deployment_is_complete = handle_deployment_completion(
            ado_express, deployment_detail, deployment_details, rollback, completed_deployments, failed_deployment_details)

        latest_deployment_status = retrieve_deployment_status(deployment_detail, ado_express, rollback)

        if latest_deployment_status is None:
            completed_deployments.append(
                deployment_detail.release_name)
            continue

        construct_and_send_deployment_status(deployment_detail, latest_deployment_status, rollback)

        if not deployment_is_complete:
            time.sleep(1)


def handle_deployment_completion(ado_express, deployment_detail, deployment_details, rollback, completed_deployments, failed_deployment_details):
    deployment_is_complete, successfully_completed = ado_express.release_deployment_completed(deployment_detail, rollback)

    if deployment_is_complete:
        completed_deployments.append(
            deployment_detail.release_name)

        if not successfully_completed:
            failed_deployment = next(x for x in deployment_details if x.release_name == deployment_detail.release_name)
            failed_deployment_details.append(failed_deployment)

    return completed_deployments, failed_deployment_details, deployment_is_complete


def retrieve_deployment_status(deployment_detail, ado_express, rollback):
    latest_deployment_status: DeploymentStatus = ado_express.get_deployment_status(deployment_detail, rollback)
    deployment_status = dict()

    if latest_deployment_status is None:
        deployment_status[deployment_detail.release_name] = DeploymentStatusSerializer('Unable to retrieve deployment status - Please check ADO', 0, 'Unknown')
        WebSocketConsumer.send_message(json.dumps({key: value.to_dict() for key, value in deployment_status.items()}), WebsocketMessageType.DeploymentStatus.value)
        return None

    return latest_deployment_status


def send_live_status_data_and_check_for_failures(deployment_details, ado_express: ADOExpress, rollback=False):
    threads = []
    failed_deployment_details = []

    for deployment_detail in deployment_details:
        thread = Thread(target=handle_deployment_and_send_status, args=(
            ado_express, deployment_detail, deployment_details, rollback, failed_deployment_details))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return failed_deployment_details
