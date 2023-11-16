from apps.rpa_manager.views import *
from django.urls import path

app_name = "rpa_manager"

urlpatterns = [
    path('painel/', PainelView.as_view(), name="painel"),
    path('principal/', PrincipalView.as_view(), name="principal"),
    path('historico/', HistoricosPorAeronaveView.as_view(), name='historico'),
    
    path('create_risk_assessment/', RiskAssessmentCreateView.as_view(), name='create_risk_assessment'),
    path('read_risk_assessment/<int:pk>/', RiskAssessmentDetailView.as_view(), name='read_risk_assessment'),
    path('update_risk_assessment/<int:pk>/', RiskAssessmentUpdateView.as_view(), name='update_risk_assessment'),
    path('delete_risk_assessment/<int:pk>/', RiskAssessmentDeleteView.as_view(), name='delete_risk_assessment'),
    path('generate_pdf/<int:pk>/pdf/', RiskAssessmentPDFDetailView.as_view(), name='generate_pdf'),
    path('risk_assessment_list/', RiskAssessmentListView.as_view(), name='risk_assessment_list'),
    path('create_assessment/', AssessmentCreateView.as_view(), name='create_assessment'),
    path('create_assessment/<int:risk_assessment_id>/', CreateAssessmentByRiskView.as_view(), name='create_assessment'),
    path('update_assessment/<int:pk>/', AssessmentUpdateView.as_view(), name='update_assessment'),
    path('delete_assessment/<int:pk>/', AssessmentDeleteView.as_view(), name='delete_assessment'),
    path('duplicate_risk_assessment/<int:risk_assessment_id>/', duplicate_risk_assessment, name='duplicate_risk_assessment'),

    path('create_legislation/', LegislationCreateView.as_view(), name='create_legislation'),
    path('detail_legislation/<int:pk>/', LegislationDetailView.as_view(), name='detail_legislation'),
    path('update_legislation/<int:pk>/', LegislationUpdateView.as_view(), name='update_legislation'),
    path('delete_legislation/<int:pk>/', LegislationDeleteView.as_view(), name='delete_legislation'),
    
    path('create_incidente/', IncidentesCreateView.as_view(), name='create_incidente'),
    path('incidentes_detail/<int:pk>/', IncidentesDetailView.as_view(), name='incidentes_detail'),
    path('update_incidente/<int:pk>/', IncidentesUpdateView.as_view(), name='update_incidente'),
    path('delete_incidentes/<int:pk>/', IncidentesDeleteView.as_view(), name='delete_incidente'),
    path('delete_image/<int:pk>/', IncidenteImageDeleteView.as_view(), name='delete_image'),
    
    path('typeofbatteries/', TypeOfBatteryView.as_view(), name='typeofbatteries'),
    path('add_typeofbattery/', TypeOfBatteryCreateView.as_view(), name='add_typeofbattery'),
    path('edit_typeofbattery/<int:pk>', TypeOfBatteryUpdateView.as_view(), name='edit_typeofbattery'),
    path('delete_typeofbattery/<int:pk>', TypeOfBatteryDeleteView.as_view(), name='delete_typeofbattery'),
    
    path('list_points/', PointsOfInterestView.as_view() , name='points_of_interest'),
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
    path('criar_novo_relatorio/<int:pk>', CriarNovoRelatorioView.as_view(), name="criar_novo_relatorio"),
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
    path('delete_image_checklist/<int:pk>/', ChecklistImageDeleteView.as_view(), name='delete_image_checklist'),

    path('checklists/', ChecklistsView.as_view(), name="checklists"),
    path('aeronaves/', AeronavesView.as_view(), name="aeronaves"),
    path('relatorios/', RelatoriosView.as_view(), name="relatorios"),
    path('baterias/', BateriasView.as_view(), name="baterias"),
    path('incidentes/', IncidentesView.as_view(), name="incidentes"),
    path('legislations/', LegislationsView.as_view(), name="legislations"),
]
