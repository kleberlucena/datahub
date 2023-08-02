from django.urls import path

from . import views

app_name = 'auth_oidc'

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('info_user_inactivate', views.InfoUserInactivateView.as_view(),
         name='info_user_inactivate'),
    path('task-entity-api-portal/', views.TaskUpdateSocialAccountsView.as_view(), name='task_update_social_accounts'),
    path('command_portal/', views.ComandsAPIAuthOidcView.as_view(), name='command_auth_oidc'),
    path('info_user_inactivate', views.InfoUserInactivateView.as_view(), name='info_user_inactivate'),
]
