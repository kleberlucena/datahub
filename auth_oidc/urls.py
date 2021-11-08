from django.urls import path

from auth_oidc.views import logout

app_name = 'auth_oidc'

urlpatterns = [
    path('logout', logout, name='logout'),
]