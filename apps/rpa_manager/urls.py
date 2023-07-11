from django.urls import path

from .views import views_main
from .views.views_main import (
    PainelView, PrincipalView,
    ChecklistsView, RelatoriosView,
    EfetivoView, AeronavesView,
    BateriasView, VerMissaoView,
    CriarNovaMissaoView,EditarMissaoView, 
    EventoDeleteView, CriarNovoRelatorioView,
    VerRelatorioView,
    EditarRelatorioView, DeletarRelatorioView,
    VerEfetivoView, CriarNovoMilitarView,
    EditarEfetivoView, DeletarEfetivoView,
    )

app_name = "rpa_manager"

urlpatterns = [
    path('painel/', PainelView.as_view(), name="painel"),
    path('principal/', PrincipalView.as_view(), name="principal"),

    path('ver_missao/<int:pk>/', VerMissaoView.as_view(), name="ver_missao"),
    path('criar_nova_missao/', CriarNovaMissaoView.as_view(), name="criar_nova_missao"),
    path('editar_missao/<int:pk>/', EditarMissaoView.as_view(), name="editar_missao"),
    path('deletar_missao/<int:pk>/', EventoDeleteView.as_view(), name="deletar_missao"),

    path('ver_relatorio/<int:pk>/', VerRelatorioView.as_view(), name="ver_relatorio"),
    path('criar_novo_relatorio/<int:pk>/', CriarNovoRelatorioView.as_view(), name="criar_novo_relatorio"),
    path('editar_relatorio/<int:pk>/', EditarRelatorioView.as_view(), name="editar_relatorio"),
    path('deletar_relatorio/<int:pk>/', DeletarRelatorioView.as_view(), name="deletar_relatorio"),

    path('ver_aeronave/<int:pk>/', views_main.ver_aeronave, name="ver_aeronave"),
    path('criar_nova_aeronave/', views_main.criar_nova_aeronave, name="criar_nova_aeronave"),
    path('editar_aeronave/<int:pk>/', views_main.editar_aeronave, name="editar_aeronave"),
    path('deletar_aeronave/<int:pk>/', views_main.deletar_aeronave, name="deletar_aeronave"),

    path('ver_bateria/<int:pk>/', views_main.ver_bateria, name="ver_bateria"),
    path('criar_nova_bateria/', views_main.criar_nova_bateria, name="criar_nova_bateria"),
    path('editar_bateria/<int:pk>/', views_main.editar_bateria, name="editar_bateria"),
    path('deletar_bateria/<int:pk>/', views_main.deletar_bateria, name="deletar_bateria"),

    path('checklists/', ChecklistsView.as_view(), name="checklists"),
    path('checklist_form/', views_main.checklist_form, name="checklist_form"),
    path('ver_checklist/<int:pk>/', views_main.ver_checklist, name="ver_checklist"),
    path('editar_checklist/<int:pk>/', views_main.editar_checklist, name="editar_checklist"),
    path('deletar_checklist/<int:pk>/', views_main.deletar_checklist, name="deletar_checklist"),

    path('efetivo/', EfetivoView.as_view(), name="efetivo"),
    path('criar_novo_militar/', CriarNovoMilitarView.as_view(), name="criar_novo_militar"),
    path('ver_efetivo/<int:pk>/', VerEfetivoView.as_view(), name="ver_efetivo"),
    path('editar_efetivo/<int:pk>/', EditarEfetivoView.as_view(), name="editar_efetivo"),
    path('deletar_efetivo/<int:pk>/', DeletarEfetivoView.as_view(), name="deletar_efetivo"),

    path('aeronaves/', AeronavesView.as_view(), name="aeronaves"),
    path('relatorios/', RelatoriosView.as_view(), name="relatorios"),
    path('baterias/', BateriasView.as_view(), name="baterias"),
]
