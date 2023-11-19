from django.http import HttpResponseRedirect
from apps.rpa_manager.forms import *
from apps.rpa_manager.models import *
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from apps.rpa_manager.utils.createJsonByLastReport import createJsonByLastReport
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from base.mixins import GroupRequiredMixin
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission
from django.contrib import messages
from django.utils import timezone

MESSAGE_MODEL_NAME = 'Caderneta'


class VerRelatorioView(GroupRequiredMixin, DetailView):
    model = Report
    template_name = 'rpa_manager/detail_report.html'
    context_object_name = 'relatorio'
    group_required = ['profile:rpa_view', 'profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            relatorio = self.get_object()
            coordinates_json = {}
            context['coordinates_json'] = createJsonByLastReport(coordinates_json, relatorio)

            return context
        
        
class CriarNovoRelatorioView(GroupRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'rpa_manager/create_report.html'
    success_url = reverse_lazy('rpa_manager:add_point')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_initial(self):
        operation = get_object_or_404(Operation, pk=self.kwargs['pk'])
        return {
            'title': operation.title,
            'remote_pilot': self.request.user,
            'observer_pilot': operation.observer_pilot,
            'who_requested': operation.who_requested,
            'who_authorized': operation.who_authorized,
            'location': operation.location,
            'latitude': operation.latitude,
            'longitude': operation.longitude,
            'operation_report': 'Sem alteração',
            'aircraft': operation.aircraft,
        }
        
    def form_valid(self, form):
        self.object = self.get_context_data()
        operation = get_object_or_404(Operation, pk=self.kwargs['pk'])
        operation.completed = True
        operation.save()

        aeronave = operation.aircraft
        aeronave.in_use = False
        aeronave.save()

        form.instance.missao = operation
        
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criada com sucesso!')
        
        return super().form_valid(form)
    
    
class EditarRelatorioView(GroupRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'rpa_manager/update_report.html'
    success_url = reverse_lazy('rpa_manager:relatorios')
    context_object_name = 'relatorio'
    group_required = ['profile:rpa_advanced']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        
        return response
            
class DeletarRelatorioView(GroupRequiredMixin, DeleteView):
    model = Report
    template_name = 'rpa_manager/delete_report.html'
    success_url = reverse_lazy('rpa_manager:relatorios')
    context_object_name = 'obj'
    group_required = ['profile:rpa_advanced']
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
        return response

