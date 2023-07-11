from django.urls import path

from .views import views_main
from .views.views_main import (
    PainelView, PrincipalView,
    ChecklistsView, RelatoriosView,
    EfetivoView, AeronavesView,
    BateriasView, 
    )

app_name = "rpa_manager"

urlpatterns = [
    path('painel/', PainelView.as_view(), name="painel"),
    path('principal/', PrincipalView.as_view(), name="principal"),
    path('criar_nova_missao/', views_main.criar_nova_missao, name="criar_nova_missao"),
    path('criar_novo_relatorio/<int:id>/', views_main.criar_novo_relatorio, name="criar_novo_relatorio"),
    path('checklist_form/', views_main.checklist_form, name="checklist_form"),
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
    path('aeronaves/', AeronavesView.as_view(), name="aeronaves"),
    path('relatorios/', RelatoriosView.as_view(), name="relatorios"),
    path('checklists/', ChecklistsView.as_view(), name="checklists"),
    path('efetivo/', EfetivoView.as_view(), name="efetivo"),
    path('baterias/', BateriasView.as_view(), name="baterias"),
]