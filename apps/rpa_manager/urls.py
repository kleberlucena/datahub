from django.urls import path

from .views import views_main

app_name = "rpa_manager"

urlpatterns = [
    path('painel/', views_main.painel, name="painel"),
    path('principal/', views_main.principal, name="principal"),
    path('dashboard/', views_main.dashboard, name="dashboard"),
    path('criar_nova_missao/', views_main.criar_nova_missao, name="criar_nova_missao"),
    path('criar_novo_relatorio/<int:id>/', views_main.criar_novo_relatorio, name="criar_novo_relatorio"),
    path('criar_novo_militar/', views_main.criar_novo_militar, name="criar_novo_militar"),
    path('criar_nova_aeronave/', views_main.criar_nova_aeronave, name="criar_nova_aeronave"),
    path('criar_nova_bateria/', views_main.criar_nova_bateria, name="criar_nova_bateria"),
    path('deletar_missao/<int:id>/', views_main.deletar_missao, name="deletar_missao"),
    path('ver_missao/<int:id>/', views_main.ver_missao, name="ver_missao"),
    path('ver_relatorio/<int:id>/', views_main.ver_relatorio, name="ver_relatorio"),
    path('ver_checklist/<int:id>/', views_main.ver_checklist, name="ver_checklist"),
    path('ver_efetivo/<int:id>/', views_main.ver_efetivo, name="ver_efetivo"),
    path('ver_aeronave/<int:id>/', views_main.ver_aeronave, name="ver_aeronave"),
    path('ver_bateria/<int:id>/', views_main.ver_bateria, name="ver_bateria"),
    path('editar_relatorio/<int:id>/', views_main.editar_relatorio, name="editar_relatorio"),
    path('editar_missao/<int:id>/', views_main.editar_missao, name="editar_missao"),
    path('editar_checklist/<int:id>/', views_main.editar_checklist, name="editar_checklist"),
    path('editar_efetivo/<int:id>/', views_main.editar_efetivo, name="editar_efetivo"),
    path('editar_aeronave/<int:id>/', views_main.editar_aeronave, name="editar_aeronave"),
    path('editar_bateria/<int:id>/', views_main.editar_bateria, name="editar_bateria"),
    path('deletar_checklist/<int:id>/', views_main.deletar_checklist, name="deletar_checklist"),
    path('deletar_relatorio/<int:id>/', views_main.deletar_relatorio, name="deletar_relatorio"),
    path('deletar_efetivo/<int:id>/', views_main.deletar_efetivo, name="deletar_efetivo"),
    path('deletar_aeronave/<int:id>/', views_main.deletar_aeronave, name="deletar_aeronave"),
    path('deletar_bateria/<int:id>/', views_main.deletar_bateria, name="deletar_bateria"),
    path('aeronaves/', views_main.aeronaves, name="aeronaves"),
    path('relatorios/', views_main.relatorios, name="relatorios"),
    path('checklists/', views_main.checklists, name="checklists"),
    path('checklist_form/', views_main.checklist_form, name="checklist_form"),
    path('efetivo/', views_main.efetivo, name="efetivo"),
    path('baterias/', views_main.baterias, name="baterias"),
    path('obtem_dados_de_missoes_por_mes/', views_main.obtem_dados_de_missoes_por_mes, name="obtem_dados_de_missoes_por_mes"),
    path('obtem_dados_de_missoes_por_usuario/', views_main.obtem_dados_de_missoes_por_usuario, name="obtem_dados_de_missoes_por_usuario"),
]