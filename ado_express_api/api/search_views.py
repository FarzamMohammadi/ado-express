from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RunConfigurationsSerializer
import status

# @api_view(['GET'])
# def getData(request):
#     deployments = RunConfigurations(crucial_release_definitions= ['3210','asdf'], organization_url='str', target='321', personal_access_token='str', queries= ['12','32'], release_name_format= 'str', release_target_env= 'str', search_only= True, via_env= False, via_env_source_name= 'str', via_env_latest_release= 'str')
#     serializer = RunConfigurationsSerializer(deployments, many=True)
  
#     return Response(serializer.data)

@api_view(['POST'])
def search_via_query(request):
    serializer = RunConfigurationsSerializer(data=request.data)
    serializer.fields['queries'].required = True

    if serializer.is_valid():
        print('valid')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Fields are invalid")
        
  
    return Response(serializer.data)