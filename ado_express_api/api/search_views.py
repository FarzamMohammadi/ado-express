import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

from base.models.RunConfigurations import RunConfigurations
from .serializers import RunConfigurationsSerializer
import status
from ado_express.main import Startup

# @api_view(['GET'])
# def getData(request):
#     deployments = RunConfigurations(crucial_release_definitions= ['3210','asdf'], organization_url='str', target='321', personal_access_token='str', queries= ['12','32'], release_name_format= 'str', release_target_env= 'str', search_only= True, via_env= False, via_env_source_name= 'str', via_env_latest_release= 'str')
#     serializer = RunConfigurationsSerializer(deployments, many=True)
  
#     return Response(serializer.data)

@api_view(['POST'])
def search_via_query(request):
    serializer = RunConfigurationsSerializer(data=request.data)
    # Fields required for query run
    serializer.fields['queries'].required = True
    serializer.fields['release_target_env'].required = True
    serializer.fields['via_env'].required = True
    serializer.fields['via_env_source_name'].required = True

    if serializer.is_valid():
        run_configurations = RunConfigurations(serializer.validated_data['explicit_release_values'], 
                                               serializer.validated_data['crucial_release_definitions'], 
                                               serializer.validated_data['organization_url'], 
                                               serializer.validated_data['personal_access_token'], 
                                               serializer.validated_data['queries'], 
                                               serializer.validated_data['release_name_format'], 
                                               serializer.validated_data['release_target_env'], 
                                               serializer.validated_data['search_only'], 
                                               serializer.validated_data['via_env'], 
                                               serializer.validated_data['via_env_latest_release'],
                                               serializer.validated_data['via_env_source_name'])
        
        startup_runners = Startup(run_configurations)
        deployment_details = startup_runners.get_deployment_details_from_query()

        return Response(status=status.HTTP_200_OK, data={'releases': json.dumps([ob.__dict__ for ob in deployment_details])})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=f"Fields are invalid{serializer.error_messages}")