import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import status
from api.utils.snake_to_camel import SnakeToCamelCaseConverter
from base.models.DeploymentDetail import DeploymentDetail
from base.models.enums.WebsocketMessageType import WebsocketMessageType
from base.models.ReleaseDetail import ReleaseDetail
from base.models.RunConfiguration import RunConfiguration
from rest_framework.decorators import api_view
from rest_framework.response import Response
from websocket_server.consumers.consumers import WebSocketConsumer

from ado_express.main import ADOExpress

from .serializers import (DeploymentDetailSerializer,
                          DeploymentStatusSerializer,
                          GenericWebsocketMessageSerializer,
                          RunConfigurationSerializer)


@api_view(['POST'])
def search_via_release_environment(request):
    request_data, error = setup_serializer_and_validate(request, RunConfigurationSerializer.set_field_requirements_for_via_environment)

    if error:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error)

    run_configurations = initialize_run_configuration(
        request_data, None, True, False)
    ado_express = ADOExpress(run_configurations)

    result = process_search(
        ado_express,
        run_configurations.deployment_details,
        process_search_via_release_environment,
        f"\n\nInitiating search to identify the most recent releases within the designated target environment: {run_configurations.RELEASE_TARGET_ENV}",
        False
    )

    return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(result))


@api_view(['POST'])
def search_via_latest_release(request):
    request_data, error = setup_serializer_and_validate(request, RunConfigurationSerializer.set_field_requirements_for_via_latest)

    if error:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error)

    run_configurations = initialize_run_configuration(
        request_data, None, True, True)
    ado_express = ADOExpress(run_configurations)

    result = process_search(
        ado_express,
        run_configurations.deployment_details,
        process_search_via_latest_release,
        f"\n\nInitiating search to identify the most recent releases within\n\nThe Source Environment: {run_configurations.VIA_ENV_SOURCE_NAME}\nTo Be Deployed to Target Environment: {run_configurations.RELEASE_TARGET_ENV}"
    )

    return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(result))


@api_view(['POST'])
def search_via_release_number(request):
    request_data, error = setup_serializer_and_validate(request, RunConfigurationSerializer.set_field_requirements_for_via_number)

    if error:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error)

    run_configurations = initialize_run_configuration(
        request_data, None, False, False)
    ado_express = ADOExpress(run_configurations)

    result = process_search(
        ado_express,
        run_configurations.deployment_details,
        process_search_via_release_number,
        f"\n\nInitiating retrieval of corresponding release information based provided release numbers",
        False
    )

    return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(result))


@api_view(['POST'])
def search_via_query(request):
    request_data, error = setup_serializer_and_validate(request, RunConfigurationSerializer.set_field_requirements_for_via_query)

    if error:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error)

    run_configurations = initialize_run_configuration(
        request_data, request_data['queries'], True, True)
    ado_express = ADOExpress(run_configurations)

    result = process_search(
        ado_express,
        None,
        process_search_via_query,
        f"\n\nInitiating search to identify the most recent releases based on the provided queries within\n\nThe Source Environment: {run_configurations.VIA_ENV_SOURCE_NAME}\nTo Be Deployed to Target Environment: {run_configurations.RELEASE_TARGET_ENV}"
    )

    return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(result))


def calculate_search_duration(search_start_time):
    search_end_time = datetime.now()
    total_search_time = round(
        (search_end_time - search_start_time).total_seconds())
    return total_search_time


def delayed_function_call(delay, func, args):
    def delayed_call():
        time.sleep(delay)
        func(*args)
    thread = threading.Thread(target=delayed_call)
    thread.start()


def initialize_run_configuration(request_data, queries, via_env, via_env_latest_release):
    run_configurations = RunConfiguration(
        None,
        None,
        request_data['organization_url'],
        request_data['personal_access_token'],
        queries,
        request_data['release_name_format'],
        request_data['release_target_env'],
        True,    # search_only
        via_env,
        via_env_latest_release,
        request_data['via_env_source_name'],
        request_data['deployment_details'])

    return run_configurations


def process_search(ado_express, deployment_details, process_search_function, initiation_message, finding_deployments=True):
    details = dict()

    send_generic_message(initiation_message, True)
    search_start_time = datetime.now()

    with ThreadPoolExecutor(max_workers=50) as executor:
        if (deployment_details):
            futures = [executor.submit(process_search_function, deployment_detail, ado_express)
                       for deployment_detail in deployment_details]

            for future in as_completed(futures):
                result = future.result()

                if result:
                    details[result[0]] = result[1]

            finalization_message = f"\n\nSearch is now complete.\n\nSearch Time: {calculate_search_duration(search_start_time)} seconds\nSearched Releases: {len(deployment_details)}\n{'Found Deployments: ' + str(len(details)) if finding_deployments else 'Found Releases: ' + str(len(details))}\n\nHave a great day!"

        else:
            details = process_search_function(ado_express)

            if not details or len(details) == 0:
                send_generic_message(
                    f"\n\nResults not found. Please check your run configuration.", False)
            # TODO: would be cool to add a -Releases Scope: NAME OF QUERY- here
            finalization_message = f"\n\nSearch is now complete.\n\nSearch Time: {calculate_search_duration(search_start_time)} seconds\nFound Deployments: {len(details)}\n\nHave a great day!"

    delayed_function_call(2, send_generic_message, [
                          finalization_message, False])

    return details


def process_search_via_latest_release(deployment, ado_express):
    converted_deployment_details = DeploymentDetail(
        deployment['release_project_name'], deployment['release_name'], None, None, deployment['is_crucial'])

    deployment_detail = ado_express.get_deployment_detail_from_latest_release(
        converted_deployment_details)

    if deployment_detail:
        return (deployment['release_name'], deployment_detail.__dict__)

    return None


def process_search_via_release_environment(deployment, ado_express):
    converted_deployment_details = DeploymentDetail(
        deployment['release_project_name'], deployment['release_name'], None, None, False)

    releases: list[ReleaseDetail] = ado_express.search_and_log_details_only(
        converted_deployment_details)

    if releases:
        return (deployment['release_name'], [release.__dict__ for release in releases])

    return None


def process_search_via_release_number(deployment, ado_express):
    converted_deployment_details = DeploymentDetail(
        deployment['release_project_name'], deployment['release_name'], deployment['release_number'], None, deployment['is_crucial'])

    releases: list[ReleaseDetail] = ado_express.search_and_log_details_only(
        converted_deployment_details)

    if releases:
        return (deployment['release_name'], [release.__dict__ for release in releases])

    return None


def process_search_via_query(ado_express):
    deployment_details = dict()
    deployment_details_list = ado_express.get_deployment_details_from_query()

    for deployment in deployment_details_list:
        deployment_details[deployment.release_name] = deployment.__dict__

    return deployment_details


def send_generic_message(message: str, showIdleDots: bool = False):
    message = GenericWebsocketMessageSerializer(message, showIdleDots)
    WebSocketConsumer.send_message(json.dumps(
        message.to_dict()), WebsocketMessageType.Generic.value)


def setup_serializer_and_validate(request, set_run_configuration_field_requirements_function):
    run_config_serializer = RunConfigurationSerializer(data=request.data)

    if set_run_configuration_field_requirements_function: set_run_configuration_field_requirements_function(run_config_serializer)

    if run_config_serializer.is_valid():
        request_data = run_config_serializer.validated_data
        return request_data, None
    else:
        return None, f"Errors:\n{run_config_serializer.errors}"