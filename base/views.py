from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group



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

class IndexView(TemplateView):
    def get(self, request):
        user = request.user
        group_list = Group.objects.filter(user=user).values()
        if any("fact" in item['name'] for item in group_list):
            return redirect('fact:index')

        if any("profile:person" in item['name'] for item in group_list):
            return redirect('person:list_person')

        return render(request, 'base/index.html',)


class AboutView(TemplateView):
    template_name = 'base/about.html'


def authorization_error_view(request):
    return render(request, 'base/error_template.html', {'message': 'Você não tem permissão para acessar essa página'})
