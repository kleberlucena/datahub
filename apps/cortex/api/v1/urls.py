from django.urls import path

from apps.cortex.api.v1.viewsets import *

app_name = 'cortex'

urlpatterns = [
    # Pessoas
    # http://localhost:8000/cortex/pessoas/cpf/71888858427/
    path('pessoas/cpf/<str:cpf>/', PessoaByCpfViewSet.as_view(), name='pessoa_cpf'),
    path('pessoas/mae/', PessoaByMotherViewSet.as_view(), name='pessoa_mae'),
    path('pessoas/nascimento/', PessoaByBirthdateViewSet.as_view(), name='pessoa_nascimento'),
    path('pessoas/<uuid:uuid>/', PersonRetrieveView.as_view(), name='pessoa_cpf'),
]