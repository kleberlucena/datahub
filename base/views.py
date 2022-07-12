from django.http import HttpResponse
from django.views.generic import TemplateView

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
