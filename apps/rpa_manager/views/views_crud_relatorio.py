from django.http import HttpResponseRedirect
from apps.rpa_manager.forms import RelatorioFormulario
from apps.rpa_manager.models import Missao, Relatorio
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
    model = Relatorio
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
    model = Relatorio
    form_class = RelatorioFormulario
    template_name = 'rpa_manager/create_report.html'
    success_url = reverse_lazy('rpa_manager:add_point')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_initial(self):
        missao = get_object_or_404(Missao, pk=self.kwargs['pk'])
        return {
            'titulo': missao.titulo,
            'militar': self.request.user,
            'piloto_observador': missao.piloto_observador,
            'quem_solicitou': missao.quem_solicitou,
            'quem_autorizou': missao.quem_autorizou,
            'local': missao.local,
            'latitude': missao.latitude,
            'longitude': missao.longitude,
            'relato_da_missao': 'Sem alteração',
            'aeronave': missao.aeronave,
        }
        
    def form_valid(self, form):
        self.object = self.get_context_data()
        missao = get_object_or_404(Missao, pk=self.kwargs['pk'])
        missao.concluida = True
        missao.save()

        aeronave = missao.aeronave
        aeronave.em_uso = False
        aeronave.save()

        form.instance.missao = missao
        
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criada com sucesso!')
        
        return super().form_valid(form)
    
    
class EditarRelatorioView(GroupRequiredMixin, UpdateView):
    model = Relatorio
    form_class = RelatorioFormulario
    template_name = 'rpa_manager/update_report.html'
    success_url = reverse_lazy('rpa_manager:relatorios')
    context_object_name = 'relatorio'
    group_required = ['profile:rpa_advanced']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        
        return response

    def dispatch(self, *args, **kwargs):
        relatorio = self.get_object()
        time_since_creation = timezone.now() - relatorio.created_at
        if time_since_creation.total_seconds() > 24 * 60 * 60:  # 24 horas em segundos
            messages.error(self.request, 'Não é possível editar esta Caderneta após 24 horas.')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(*args, **kwargs)
    
    
class DeletarRelatorioView(PermissionRequiredMixin, DeleteView):
    model = Relatorio
    template_name = 'rpa_manager/delete_report.html'
    success_url = reverse_lazy('rpa_manager:relatorios')
    context_object_name = 'obj'
    permission_required = 'rpa_manager.delete_relatorio'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        relatorio = self.get_object()
        time_since_creation = timezone.now() - relatorio.created_at
        if time_since_creation.total_seconds() > 24 * 60 * 60:  # 24 horas em segundos
            messages.error(self.request, 'Não é possível excluir esta Caderneta após 24 horas.')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(*args, **kwargs)
