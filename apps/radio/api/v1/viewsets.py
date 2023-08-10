from rest_framework import generics
from rest_framework.response import Response
from rest_framework import generics, permissions
import logging

from apps.radio.api.v1.serializers import GpsSerializer
from apps.radio.models import Gps
from apps.radio.tasks import send_gps_to_bacinf

# Get an instance of a logger
logger = logging.getLogger(__name__)

class GpsViewSet(generics.ListCreateAPIView):
    queryset = Gps.objects.all()
    serializer_class = GpsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ipaddress = self.request.META.get("REMOTE_ADDR")
        remote_host = self.request.META.get("REMOTE_HOST")
        http_user_agent = self.request.META.get("HTTP_USER_AGENT")
        dados = self.request.data
        if serializer.is_valid():
            instance = serializer.save(dados=dados, ipaddress=ipaddress, remote_host=remote_host, http_user_agent=http_user_agent, user=self.request.user.username)
            if instance:
                dados_salvos = self.get_serializer(instance).data
                try:
                    print(dados_salvos['dados'])
                    send_gps_to_bacinf.delay(dados=dados_salvos['dados'])
                    logger.info('Send gps position to bacinf')
                except Exception as e:
                    logger.error('Error while post gps position - {}'.format(e))
                return Response(status=201)
        return Response(serializer.errors, status=400)
