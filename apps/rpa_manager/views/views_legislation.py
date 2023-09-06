from apps.rpa_manager.models import Legislation
from apps.rpa_manager.forms import LegislationForm
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from base.mixins import GroupRequiredMixin

MESSAGE_MODEL_NAME = 'Legislação'


class LegislationCreateView(GroupRequiredMixin, CreateView):
    model = Legislation
    form_class = LegislationForm
    template_name = 'rpa_manager/create_legislation.html'
    success_url = reverse_lazy('rpa_manager:legislations')
    group_required = ['profile:rpa_advanced']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criada com sucesso!')
        return response

    
class LegislationUpdateView(GroupRequiredMixin, UpdateView):
    model = Legislation
    form_class = LegislationForm
    template_name = 'rpa_manager/update_legislation.html'
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:legislations')
    group_required = ['profile:rpa_advanced']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        return response
    
    
class LegislationDeleteView(GroupRequiredMixin, DeleteView):
    model = Legislation
    template_name = 'rpa_manager/delete_legislation.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:legislations')
    group_required = ['profile:rpa_advanced']
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
        return response
    

