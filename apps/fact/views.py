from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import *
from base.mixins import *
from base.views import *


from .models import Fact



class FactImageListView(ListView):
    model = FactImage
    template_name = 'fact_image_list.html'
    context_object_name = 'fact_images'

class FactImageCreateView(CreateView):
    model = Fact
    form_class = FactForm
    template_name = 'fact_image_form.html'
    success_url = reverse_lazy('fact-image-list')

class FactImageUpdateView(UpdateView):
    model = FactImage
    form_class = FactForm
    template_name = 'fact_image_form.html'
    success_url = reverse_lazy('fact-image-list')

class FactImageDeleteView(DeleteView):
    model = FactImage
    template_name = 'fact_image_confirm_delete.html'
    success_url = reverse_lazy('fact-image-list')


class FactTypeListView(ListView):
    model = FactType
    template_name = 'fact_type_list.html'
    context_object_name = 'fact_types'

class FactTypeCreateView(CreateView):
    model = FactType
    form_class = FactForm
    template_name = 'fact_type_form.html'
    success_url = reverse_lazy('fact-type-list')

class FactTypeUpdateView(UpdateView):
    model = FactType
    form_class = FactForm
    template_name = 'fact_type_form.html'
    success_url = reverse_lazy('fact-type-list')

class FactTypeDeleteView(DeleteView):
    model = FactType
    template_name = 'fact_type_confirm_delete.html'
    success_url = reverse_lazy('fact-type-list')


class FactListView(ListView):
    model = Fact
    template_name = 'fact_list.html'
    context_object_name = 'facts'

class FactCreateView(CreateView):
    model = Fact
    form_class = FactForm
    template_name = 'fact_form.html'
    success_url = reverse_lazy('fact-list')

class FactUpdateView(UpdateView):
    model = Fact
    form_class = FactForm
    template_name = 'fact_form.html'
    success_url = reverse_lazy('fact-list')

class FactDeleteView(DeleteView):
    model = Fact
    template_name = 'fact_confirm_delete.html'
    success_url = reverse_lazy('fact-list')


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
