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

from ado_express.main import Startup

from .serializers import (DeploymentDetailSerializer,
                          GenericWebsocketMessageSerializer,
                          RunConfigurationSerializer)


@api_view(['POST'])
def search_via_release_environment(request):
    deployment_details = DeploymentDetailSerializer()
    deployment_details.set_required_fields_for_via_environment()

    serializer = RunConfigurationSerializer(data=request.data)
    serializer.fields['deploymentDetails'].child = deployment_details

    # Fields required for via environment run
    serializer.fields['deploymentDetails'].allow_empty = False
    # Fields not required for via environment run
    serializer.fields['searchOnly'].required = False
    serializer.fields['viaEnv'].required = False
    serializer.fields['viaEnvLatestRelease'].required = False

    if serializer.is_valid():
        run_configurations = RunConfiguration(
            None,
            None,
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

        ado_express = Startup(run_configurations)
        release_details = dict()

        send_generic_message(f"\n\nInitiating search to identify the most recent releases within the designated target environment: {run_configurations.RELEASE_TARGET_ENV}", True)
        search_start_time = datetime.now()

        def process_deployment(deployment):
            converted_deployment_details = DeploymentDetail(
                deployment['release_project_name'], deployment['release_name'], None, None, False)

            releases: list[ReleaseDetail] = ado_express.search_and_log_details_only(
                converted_deployment_details)

            if releases:
                return (deployment['release_name'], [release.__dict__ for release in releases])

            return None

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(process_deployment, deployment)
                       for deployment in run_configurations.deployment_details]

            for future in as_completed(futures):
                result = future.result()

                if result:
                    release_details[result[0]] = result[1]

        search_end_time = datetime.now()
        total_search_time = round((search_end_time - search_start_time).total_seconds())

        delayed_function_call(2, send_generic_message, [f"\n\nSearch is now complete. Total Search Time: {total_search_time} seconds"])

        return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(release_details))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Errors:\n{serializer.errors}")


@api_view(['POST'])
def search_via_latest_release(request):
    deployment_details = DeploymentDetailSerializer()
    deployment_details.set_required_fields_for_via_latest()

    serializer = RunConfigurationSerializer(data=request.data)
    serializer.fields['deploymentDetails'].child = deployment_details

    # Fields required for via latest run
    serializer.fields['deploymentDetails'].allow_empty = True
    serializer.fields['releaseTargetEnv'].required = True
    serializer.fields['viaEnvSourceName'].required = True
    # Fields not required for via latest run
    serializer.fields['searchOnly'].required = False
    serializer.fields['viaEnv'].required = False
    serializer.fields['viaEnvLatestRelease'].required = False

    if serializer.is_valid():
        run_configurations = RunConfiguration(
            None,
            None,
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

        ado_express = Startup(run_configurations)
        deployment_details = dict()

        send_generic_message(f"\n\nInitiating search to identify the most recent releases within the designated target environment: {run_configurations.RELEASE_TARGET_ENV}", True)
        search_start_time = datetime.now()

        def process_deployment(deployment):
            converted_deployment_details = DeploymentDetail(
                deployment['release_project_name'], deployment['release_name'], None, None, deployment['is_crucial'])

            deployment_detail = ado_express.get_deployment_detail_from_latest_release(
                converted_deployment_details)

            if deployment_detail:
                return (deployment['release_name'], deployment_detail.__dict__)

            return None

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(process_deployment, deployment)
                       for deployment in run_configurations.deployment_details]

            for future in as_completed(futures):
                result = future.result()

                if result:
                    deployment_details[result[0]] = result[1]

        search_end_time = datetime.now()
        total_search_time = round((search_end_time - search_start_time).total_seconds())

        delayed_function_call(2, send_generic_message, [f"\n\nSearch is now complete.\n\nSearch Time: {total_search_time} seconds\nReleases Searched: {len(run_configurations.deployment_details)}\nDeployments Found: {len(deployment_details)}"])

        return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(deployment_details))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Errors:\n{serializer.errors}")


@api_view(['POST'])
def search_via_release_number(request):
    deployment_details = DeploymentDetailSerializer()
    deployment_details.set_required_fields_for_via_number()

    serializer = RunConfigurationSerializer(data=request.data)
    serializer.fields['deploymentDetails'].child = deployment_details

    # Fields required for via number run
    serializer.fields['deploymentDetails'].allow_empty = True
    # Fields not required for via number run
    serializer.fields['searchOnly'].required = False
    serializer.fields['viaEnv'].required = False
    serializer.fields['viaEnvLatestRelease'].required = False
    serializer.fields['releaseTargetEnv'].allow_blank = True
    serializer.fields['viaEnvSourceName'].allow_blank = True

    if serializer.is_valid():
        run_configurations = RunConfiguration(
            None,  # explicit_release_values
            None,  # crucial_release_definitions
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

        ado_express = Startup(run_configurations)
        release_details = dict()

        send_generic_message(f"\n\nInitiating search to identify the most recent releases within the designated target environment: {run_configurations.RELEASE_TARGET_ENV}", True)
        search_start_time = datetime.now()


        def process_deployment(deployment):
            converted_deployment_details = DeploymentDetail(
                deployment['release_project_name'], deployment['release_name'], deployment['release_number'], None, deployment['is_crucial'])

            releases: list[ReleaseDetail] = ado_express.search_and_log_details_only(
                converted_deployment_details)

            if releases:
                return (deployment['release_name'], [release.__dict__ for release in releases])

            return None

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(process_deployment, deployment)
                       for deployment in run_configurations.deployment_details]

            for future in as_completed(futures):
                result = future.result()

                if result:
                    release_details[result[0]] = result[1]

        search_end_time = datetime.now()
        total_search_time =  round(search_end_time - search_start_time)

        delayed_function_call(2, send_generic_message, [f"\n\nSearch is now complete. Total Search Time: {total_search_time} seconds"])

        return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(release_details))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid.\n{serializer.errors}")


@api_view(['POST'])
def search_via_query(request):
    serializer = RunConfigurationSerializer(data=request.data)

    # Fields required for query run
    serializer.fields['queries'].required = True
    serializer.fields['releaseTargetEnv'].required = True
    serializer.fields['viaEnv'].required = True
    # Fields not required for query run
    serializer.fields['searchOnly'].required = False

    if serializer.is_valid():
        run_configurations = RunConfiguration(
            None,
            None,
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

        ado_express = Startup(run_configurations)
        deployment_details = dict()

        send_generic_message(f"\n\nInitiating search to identify the most recent releases within the designated target environment: {run_configurations.RELEASE_TARGET_ENV}", True)
        search_start_time = datetime.now()

        def process_deployment(deployment):
            converted_deployment_details = DeploymentDetail(
                deployment['release_project_name'], deployment['release_name'], None, None, deployment['is_crucial'])

            deployment_detail = ado_express.get_deployment_detail_from_latest_release(
                converted_deployment_details)

            if deployment_detail:
                return (deployment['release_name'], deployment_detail.__dict__)

            return None

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(process_deployment, deployment)
                       for deployment in run_configurations.deployment_details]

            for future in as_completed(futures):
                result = future.result()

                if result:
                    deployment_details[result[0]] = result[1]

        search_end_time = datetime.now()
        total_search_time = round((search_end_time - search_start_time).total_seconds())

        delayed_function_call(2, send_generic_message, [f"\n\nSearch is now complete.\n\nSearch Time: {total_search_time} seconds\nReleases Searched: {len(run_configurations.deployment_details)}\nDeployments Found: {len(deployment_details)}"])

        return Response(status=status.HTTP_200_OK, data=SnakeToCamelCaseConverter.convert(deployment_details))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid.\n{serializer.errors}")



def send_generic_message(message: str, showIdleDots: bool = False):
    message = GenericWebsocketMessageSerializer(message, showIdleDots)
    WebSocketConsumer.send_message(json.dumps(message.to_dict()), WebsocketMessageType.Generic.value)

def delayed_function_call(delay, func, args):
    def delayed_call():
        time.sleep(delay)
        func(*args)
    thread = threading.Thread(target=delayed_call)
    thread.start()
