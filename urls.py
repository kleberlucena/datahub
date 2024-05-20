from django.urls import path

from . import views

app_name = 'datahub'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('formocorrencia/', views.formocorrenciaView.as_view(), name='formocorrencia'),
    path('formocorr_detalhe/', views.formocorr_detalheView.as_view(), name='formocorr_detalhe'),
    path('analise/', views.analiseView.as_view(), name='analise'),
    path('incidents/', views.IncidentListView.as_view(), name='incident_list'),
    path('analise_detalhe/', views.analise_detalheView.as_view(), name='analise_detalhe'),
    path('create_incidentView/', views.create_incidentView.as_view(), name='create_incidentView'),  
    path('incidents/edit/<str:CCD_key>/', views.IncidentUpdateView.as_view(), name='incident_edit'),
    path('incidents/delete/<str:CCD_key>/', views.IncidentDeleteView.as_view(), name='incident_delete'),
    path('incidents/exibir/<str:CCD_key>/', views.IncidentDetailView.as_view(), name='incident_detail'),

]


  #  path('create/', views.ExampleCreateView.as_view(), name='example-create'),
  #  path('<int:pk>/', views.ExampleDetailView.as_view(), name='example-detail'),    
  #  path('list/', views.ExampleListView.as_view(), name='example-list'),
    # path('list/datatable/', views.ExampleListDatatableView.as_view(), name='example-list-datatable'),
    # path('api-v1/list_json/', views.ExampleListJson.as_view(), name='example-list-json'),
    # path('update/<int:pk>', views.ExampleUpdateView.as_view(), name='example-update'),
    # path('delete/<int:pk>', views.ExampleDeleteView.as_view(), name='example-delete')]

#Obs.: quando for colocar uma página no ar:
# 1 - mudar o urls.py
# 2 - mudar a view
# 3 - Colocar no nav-left-content