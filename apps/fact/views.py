from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .models import *
from base.mixins import *
from base.views import *


# Create your views here.

class DashboardView(GroupRequiredMixin, TemplateView):
    template_name = 'fact/dashboard.html'
    group_required = ['fact:fact_basic',
                      'fact:fact_intermediate', 'fact:fact_advanced']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = request.user
        my_facts = Fact.objects.filter(created_by=user)[:3]
        facts = Fact.objects.all()

        context = {"my_facts": my_facts, "facts": facts,}
        return self.render_to_response(context)
