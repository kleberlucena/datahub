from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from apps.rpa_manager.forms import AeronavesForm
from apps.rpa_manager.models import Aeronave 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission

MESSAGE_MODEL_NAME = 'Aeronave'

class VerAeronaveView(PermissionRequiredMixin, DetailView):
    model = Aeronave
    template_name = 'controle/pages/ver_aeronave.html'
    context_object_name = 'aeronave'
    pk_url_kwarg = 'pk'
    permission_required = 'rpa_manager.view_aeronave'

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class CriarNovaAeronaveView(PermissionRequiredMixin, CreateView):
    model = Aeronave
    form_class = AeronavesForm
    template_name = 'controle/pages/criar_nova_aeronave.html'
    success_url = reverse_lazy('rpa_manager:aeronaves')
    permission_required = 'rpa_manager.add_aeronave'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criada com sucesso!')
        return response

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class EditarAeronaveView(PermissionRequiredMixin, UpdateView):
    model = Aeronave
    form_class = AeronavesForm
    template_name = 'controle/pages/editar_aeronave.html'
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:aeronaves')
    permission_required = 'rpa_manager.change_aeronave'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class DeletarAeronaveView(PermissionRequiredMixin, DeleteView):
    model = Aeronave
    template_name = 'controle/pages/delete_aeronave.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:aeronaves')
    permission_required = 'rpa_manager.delete_aeronave'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
