from django.conf import settings
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.http import JsonResponse
import requests
import logging
import json
import jwt

from social_django.utils import psa
from auth_oidc.models import synchronize_permissions


# Get an instance of a logger
logger = logging.getLogger(__name__)


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):

    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'
        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            jwt_token = serializer.validated_data['access_token']
            user = request.backend.do_auth(jwt_token)
        # except HTTPError as e:
        except Exception as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                decoded_token = jwt.decode(jwt_token, key=settings.KEYCLOAK_SERVER_PUBLIC_KEY, algorithms=['RS256'], audience="account")
                mapa_of_permissions = decoded_token['resource_access']
                synchronize_permissions(user, mapa_of_permissions)
                refresh = RefreshToken.for_user(user)
                response = {"refresh": str(refresh), "access": str(refresh.access_token)}
                return JsonResponse(response)
            else:
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
      
 
@api_view(['POST'])     
@permission_classes([IsAuthenticated])       
def expire_token(request):
    '''
    Remove o token de acesso quando chamada a url de expiração do token.
    '''
    try:
        user = request.user
        user.auth_token.delete()
        return Response(
            {'msg': {
                'token': 'Invalided token',
                'detail': 'O token foi invalidado com sucesso',
            }},
            status=status.HTTP_302_FOUND,
        )
    except Exception as e:
        raise logger.error('Error while remove auth_token from user - {}'.format(e))
        
    
        