from django.urls import path

from apps.bnmp.api.v1.viewsets import *

app_name = 'apps.bnmp'

urlpatterns = [
    # Alertas
    # http://localhost:8000/api/v1/alert/cortex/
    path('cpf/', PessoaByCpfViewSet.as_view(), name='list_cpf_bnmp'),
    path('explore/', BNMPExplorerViewSet.as_view(), name='explore_bnmp'),
    path('mandados/', MandadoByIdPessoaViewSet.as_view(), name='list_mandados_bnmp'),
]