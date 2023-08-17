from django.urls import path
from .views.views_crud_baterias import UpdateAllBateriasView
from .views.views_incidentes import (
    IncidentesCreateView,
    IncidentesUpdateView,
    IncidentesDeleteView,
    IncidentesDetailView,
    IncidenteImageDeleteView,
)
from .views.views_guarnicao import (
    GuarnicaoCreateView, 
    GuarnicaoUpdateView,
    GuarnicaoDeleteView,
    DescadastrarGuarnicao,
    )
from .views.views_points_of_interest import (
    AddPointOfInterest,
    UpdatePointOfInterest,
    DeletePointOfInterest    
)
from .views.views_typeofbattery import (
    TypeOfBatteryCreateView,
    TypeOfBatteryUpdateView,
    TypeOfBatteryDeleteView
)
from .views.views_main import (
    PainelView, PrincipalView,
    ChecklistsView, RelatoriosView,
    EfetivoView, AeronavesView,
    BateriasView, VerMissaoView,
    CriarNovaMissaoView,EditarMissaoView, 
    DeleteMissaoView, CriarNovoRelatorioView,
    VerRelatorioView, ChecklistFormView,
    EditarRelatorioView, DeletarRelatorioView,
    VerEfetivoView, CriarNovoMilitarView,
    EditarEfetivoView, DeletarEfetivoView,
    EditarChecklistView,DeletarChecklistView,
    VerChecklistView, VerAeronaveView,
    CriarNovaAeronaveView, EditarAeronaveView,
    DeletarAeronaveView, VerBateriaView,
    CriarNovaBateriaView, EditarBateriaView,
    DeletarBateriaView, MilitaryListJson,
    HistoricosPorAeronaveView, IncidentesView,
    TypeOfBatteryView)

app_name = "rpa_manager"

urlpatterns = [
    path('painel/', PainelView.as_view(), name="painel"),
    path('principal/', PrincipalView.as_view(), name="principal"),
    path('historico/', HistoricosPorAeronaveView.as_view(), name='historico'),
    
    path('create_incidente/', IncidentesCreateView.as_view(), name='create_incidente'),
    path('incidentes_detail/<int:pk>/', IncidentesDetailView.as_view(), name='incidentes_detail'),
    path('update_incidente/<int:pk>/', IncidentesUpdateView.as_view(), name='update_incidente'),
    path('delete_incidentes/<int:pk>/', IncidentesDeleteView.as_view(), name='delete_incidente'),
    path('delete_image/<int:pk>/', IncidenteImageDeleteView.as_view(), name='delete_image'),
    
    path('typeofbatteries/', TypeOfBatteryView.as_view(), name='typeofbatteries'),
    path('add_typeofbattery/', TypeOfBatteryCreateView.as_view(), name='add_typeofbattery'),
    path('edit_typeofbattery/<int:pk>', TypeOfBatteryUpdateView.as_view(), name='edit_typeofbattery'),
    path('delete_typeofbattery/<int:pk>', TypeOfBatteryDeleteView.as_view(), name='delete_typeofbattery'),
    
    path('add_point/', AddPointOfInterest.as_view(), name='add_point'),
    path('edit_point/<int:pk>/', UpdatePointOfInterest.as_view(), name='edit_point'),
    path('delete_point/<int:pk>/', DeletePointOfInterest.as_view(), name='delete_point'),
    
    path('descadastrar/', DescadastrarGuarnicao.as_view(), name='descadastrar_guarnicao'),
    path('guarnicao_form/', GuarnicaoCreateView.as_view(), name="guarnicao_form"),
    path('guarnicao/edit/<int:pk>/', GuarnicaoUpdateView.as_view(), name='guarnicao_edit'),
    path('guarnicao/delete/<int:pk>', GuarnicaoDeleteView.as_view(), name='guarnicao_delete'),
    
    path('ver_missao/<int:pk>/', VerMissaoView.as_view(), name="ver_missao"),
    path('criar_nova_missao/', CriarNovaMissaoView.as_view(), name="criar_nova_missao"),
    path('editar_missao/<int:pk>/', EditarMissaoView.as_view(), name="editar_missao"),
    path('deletar_missao/<int:pk>/', DeleteMissaoView.as_view(), name="deletar_missao"),

    path('ver_relatorio/<int:pk>/', VerRelatorioView.as_view(), name="ver_relatorio"),
    path('criar_novo_relatorio/', CriarNovoRelatorioView.as_view(), name="criar_novo_relatorio"),
    path('editar_relatorio/<int:pk>/', EditarRelatorioView.as_view(), name="editar_relatorio"),
    path('deletar_relatorio/<int:pk>/', DeletarRelatorioView.as_view(), name="deletar_relatorio"),

    path('ver_aeronave/<int:pk>/', VerAeronaveView.as_view(), name="ver_aeronave"),
    path('criar_nova_aeronave/', CriarNovaAeronaveView.as_view(), name="criar_nova_aeronave"),
    path('editar_aeronave/<int:pk>/', EditarAeronaveView.as_view(), name="editar_aeronave"),
    path('deletar_aeronave/<int:pk>/', DeletarAeronaveView.as_view(), name="deletar_aeronave"),

    path('ver_bateria/<int:pk>/', VerBateriaView.as_view(), name="ver_bateria"),
    path('criar_nova_bateria/',  CriarNovaBateriaView.as_view(), name="criar_nova_bateria"),
    path('editar_bateria/<int:pk>/', EditarBateriaView.as_view(), name="editar_bateria"),
    path('update_all_batteries/', UpdateAllBateriasView.as_view(), name='update_all_batteries'),
    path('deletar_bateria/<int:pk>/', DeletarBateriaView.as_view(), name="deletar_bateria"),

    path('ver_checklist/<int:pk>/', VerChecklistView.as_view(), name="ver_checklist"),
    path('checklist_form/', ChecklistFormView.as_view(), name="checklist_form"),
    path('editar_checklist/<int:pk>/', EditarChecklistView.as_view(), name="editar_checklist"),
    path('deletar_checklist/<int:pk>/', DeletarChecklistView.as_view(), name="deletar_checklist"),

    path('criar_novo_militar/', CriarNovoMilitarView.as_view(), name="criar_novo_militar"),
    path('ver_efetivo/<int:pk>/', VerEfetivoView.as_view(), name="ver_efetivo"),
    path('editar_efetivo/<int:pk>/', EditarEfetivoView.as_view(), name="editar_efetivo"),
    path('deletar_efetivo/<int:pk>/', DeletarEfetivoView.as_view(), name="deletar_efetivo"),

    path('efetivo/', EfetivoView.as_view(), name="efetivo"),
    path('checklists/', ChecklistsView.as_view(), name="checklists"),
    path('aeronaves/', AeronavesView.as_view(), name="aeronaves"),
    path('relatorios/', RelatoriosView.as_view(), name="relatorios"),
    path('baterias/', BateriasView.as_view(), name="baterias"),
    path('incidentes/', IncidentesView.as_view(), name="incidentes"),

    # API externa (vem do app portal)
    path('api-v1/military_list_json/', MilitaryListJson.as_view(), name='military_list_json'),
]
