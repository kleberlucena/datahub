import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.aido_sync_hub import helpers


# Get an instance of a logger
logger = logging.getLogger(__name__)


class SyncAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data # Use request.data em vez de request.JSON

        model_name = data['model_name']
        model_data = data['model_data']
       
        try:
            message_response = {}
            
            if model_name == 'Military':
                message_response = helpers.sync_military(model_data)
                
            elif model_name == 'Enjoyer':
                message_response = helpers.sync_enjoyer(model_data)
                
            elif model_name == 'Entity':
                message_response = helpers.sync_entity(model_data)
                
            elif model_name == 'Gender':
                message_response = helpers.sync_gender(model_data)
            
            elif model_name == 'OrganizationalHierarchy':
                message_response = helpers.sync_organizational_hierarchy(model_data)
            
            else:
                message_response["completed"] = False
                message_response["status"] = "fail"
                message_response["error"] = "Invalid model_name"
                
        except Exception as e:
            logger.error(f'[Aido Sync Hub - viewsets] SyncAPIView - {e}')
            message_response["completed"] = False
            message_response["status"] = "fail"
            message_response["error"] = f"Sync Fail: {e}"
            print("!"*50)
            print(model_data)
            print("#"*50)
        finally:
            return Response(message_response, status=status.HTTP_200_OK if message_response["completed"] else status.HTTP_428_PRECONDITION_REQUIRED)

        


        