from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa_manager.forms import BateriaForm
from apps.rpa_manager.models import Bateria
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission

MESSAGE_MODEL_NAME = 'Bateria'

class VerBateriaView(PermissionRequiredMixin, DetailView):
    model = Bateria
    template_name = 'rpa_manager/detail_battery.html'
    context_object_name = 'bateria'
    pk_url_kwarg = 'pk'
    permission_required = 'rpa_manager.view_bateria'

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class CriarNovaBateriaView(PermissionRequiredMixin, CreateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'rpa_manager/create_battery.html'
    success_url = reverse_lazy('rpa_manager:baterias')
    permission_required = 'rpa_manager.add_bateria'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criada com sucesso!')
        return response

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class EditarBateriaView(PermissionRequiredMixin, UpdateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'rpa_manager/update_battery.html'
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:baterias')
    permission_required = 'rpa_manager.change_bateria'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class DeletarBateriaView(PermissionRequiredMixin, DeleteView):
    model = Bateria
    template_name = 'rpa_manager/delete_battery.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:baterias')
    permission_required = 'rpa_manager.delete_bateria'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class UpdateAllBateriasView(View):
    template_name = 'rpa_manager/update_all_batteries.html'

    def get(self, request):
        baterias = Bateria.objects.all()
        return render(request, self.template_name, {'baterias': baterias})

    def post(self, request):
        for bateria_id, num_ciclos in request.POST.items():
            if bateria_id.isdigit():
                bateria = Bateria.objects.get(id=int(bateria_id))
                bateria.num_ciclos = int(num_ciclos)
                bateria.save()

        messages.success(self.request, f'Checklist criado com sucesso!')
        
        return redirect('rpa_manager:painel')
