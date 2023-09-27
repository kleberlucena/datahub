from django.urls import path
from . import views


app_name = 'protect_network'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('estabelishment/', views.EstablishmentView.as_view(), name='estabelishment'),
    path('employee/', views.EmployeeView.as_view(), name='employee'),
    path('working_hours/', views.WorkingHoursView.as_view(), name='working_hours'),
    path('security/', views.SecurityView.as_view(), name='security'),

]
