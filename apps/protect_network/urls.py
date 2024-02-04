from django.urls import path
from . import views



app_name = 'protect_network'

urlpatterns = [
###### API DE CARREGAR OS PONTOS DAS REDES SELECIONADOS NO FILTRO  ######
  path('',views.IndexView.as_view(), name='index'),

  path('spot', views.SpotListView.as_view(), name='spot_list'),
  path('spot/list_created', views.SpotListCreatedView.as_view(), name='spot_list_created'), 
  path('spot/add', views.CreateSpotView.as_view(), name='spot_add'),

####### API DE CARREGAR OS PONTOS DO MESMO TIPO DO SELECIONADO ######
  path('<int:pk>/spot/update', views.UpdateSpotView.as_view(), name='spot_update'),

  path('<int:pk>/spot/detail', views.DetailSpotView.as_view(), name='spot_detail'),
  path('<int:pk>/spot/detail_card', views.DetailCardSpotView.as_view(), name='spot_detail_card'),
  path('<int:pk>/spot/update/tags', views.UpdateSpotTagsView.as_view(), name='spot_tags_update'),
  path('spot_type', views.SpotTypeListView.as_view(), name='type_list'), 
  path('spot_type/add', views.CreateSpotTypeView.as_view(), name='type_add'), 
  path('<int:pk>/spot_type/update', views.UpdateSpotTypeView.as_view(), name='type_update'),
  path('tag', views.TagListView.as_view(), name='tag_list'), 
  path('tag/add', views.CreateTagView.as_view(), name='tag_add'), 
  path('<int:pk>/tag/update', views.UpdateTagView.as_view(), name='tag_update'),
  path('<int:spot_id>/contact/add', views.CreateContactInfoView.as_view(), name='contact_add'), 
  path('<int:pk>/contact/update', views.UpdateContactInfoView.as_view(), name='contact_update'),
  path('<int:pk>/contact/delete', views.DeleteContactInfoView.as_view(), name='contact_delete'),
  path('<int:spot_id>/opening_hours/add/<str:day_of_week>/', views.CreateOpeningHoursView.as_view(), name='opening_hours_add_monday'),
  path('<int:spot_id>/opening_hours/add', views.CreateOpeningHoursView.as_view(), name='opening_hours_add'), 
  path('<int:pk>/opening_hours/update', views.UpdateOpeningHoursView.as_view(), name='opening_hours_update'),
  path('<int:spot_id>/spot/image/add', views.CreateImageSpotView.as_view(), name='spot_image_add'),
  path('<int:spot_id>/spot/images', views.ImageListView.as_view(), name='spot_image_list'),
  path('spot/image/<int:pk>/delete/', views.ImageDeleteView.as_view(), name='spot_image_delete'),
  path('<int:pk>/network/detail', views.NetworkDetailView.as_view(), name='network_detail'),
  path('network', views.NetworkListView.as_view(), name='network_list'), 
  path('network/add', views.CreateNetworkView.as_view(), name='network_add'),
  path('<int:pk>/network/update', views.UpdateNetworkView.as_view(), name='network_update'),
  path('<int:pk>/responsible/add', views.CreateResponsibleView.as_view(), name='responsible_add'),
  path('<int:pk>/responsible/update', views.UpdateResponsibleView.as_view(), name='responsible_update'),
  path('<int:pk>/responsible/delete', views.DeleteResponsibleView.as_view(), name='responsible_delete'),
  path('qpp', views.QppListView.as_view(), name='qpp_list'), 
  path('qpp/add', views.CreateQppView.as_view(), name='qpp_add'), 
  path('<int:pk>/qpp/update', views.UpdateQppView.as_view(), name='qpp_update'),
  path('<int:spot_id>/survey/add', views.CreateSurveyView.as_view(), name='survey_add'),
  path('<int:pk>/survey/update', views.UpdateSurveyView.as_view(), name='survey_update'), 
  path('get_responsibles/', views.get_responsibles, name='get_responsibles'),
 
]