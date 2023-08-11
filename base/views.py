from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)


def health_check(request):
    """View function for health check"""
    logger.error("Ai dento 0")
    return HttpResponse(status=204)


class IndexView(TemplateView):
    template_name = 'base/index.html'


class AboutView(TemplateView):
    template_name = 'base/about.html'

def authorization_error_view(request):
    return render(request, 'base/error_template.html', {'message': 'Você não tem permissão para acessar essa página'})
