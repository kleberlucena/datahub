from django.urls import path

from .views import *

app_name = 'termsofuse'

urlpatterns = [
    path('sasp/', TermsSASPView.as_view(), name='sasp_terms_of_use'),
]