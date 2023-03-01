import json
import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from base.models.RunConfigurations import RunConfigurations
from base.models.DeploymentDetails import DeploymentDetails

from .serializers import RunConfigurationsSerializer, DeploymentDetailsSerializer

from ado_express.main import Startup

@api_view(['POST'])
def deploy(request):
    deployment_details_serializer = DeploymentDetailsSerializer()
    serializer = RunConfigurationsSerializer(data=request.data)

    serializer.fields['deployment_details'].child = deployment_details_serializer

    # Fields required for run
    serializer.fields['deployment_details'].allow_empty = False

    if serializer.is_valid():
        run_configurations = RunConfigurations(serializer.validated_data['explicit_release_values'], 
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
        
        startup_runners = Startup(run_configurations)
        deployment_details = []
        
        for deployment in run_configurations.deployment_details:
            converted_deployment_details = DeploymentDetails(deployment['release_project_name'], deployment['release_name'], deployment['release_number'], deployment['release_rollback'], deployment['is_crucial'])
            deployment_details.append(converted_deployment_details)
        
        explicit_deployment_details = startup_runners.updated_deployment_details_based_on_explicit_inclusion_and_exclusion(deployment_details)
        if explicit_deployment_details: deployment_details = explicit_deployment_details
        
        crucial_deployment_details = []
        # Needs to be null so get_crucial_release_definitions knows to check deployment_details instead
        if run_configurations.CRUCIAL_RELEASE_DEFINITIONS == []: run_configurations.CRUCIAL_RELEASE_DEFINITIONS = None
        
        crucial_release_definitions = startup_runners.get_crucial_release_definitions(deployment_details)
        
        if crucial_release_definitions:
            # Separate crucial & regular deployments based on release definitions that match CRUCIAL_RELEASE_DEFINITIONS env variable list
            crucial_deployment_details = startup_runners.get_crucial_deployment_from_deployment_details(deployment_details, crucial_release_definitions)
            deployment_details[:] = startup_runners.remove_crucial_deployments_from_deployment_details(deployment_details, crucial_release_definitions)

        #TODO Add clear rollback handling and return results to user - currently it's handled but user is not notified and will only know the deployment was unsuccessful 
        crucial_deployment_results = []
        regular_deployment_results = []

        if crucial_deployment_details:
            crucial_deployment_results.append(startup_runners.run_release_deployments(crucial_deployment_details, True))

        if deployment_details:
            regular_deployment_results.append(startup_runners.run_release_deployments(deployment_details, False, True))

        return Response(status=status.HTTP_200_OK, data={'crucial_deployments': json.dumps([ob.__dict__ for ob in crucial_deployment_results], default=str), 'regular_deployments': json.dumps([ob.__dict__ for ob in regular_deployment_results], default=str)})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid.\n{serializer.error_messages}")