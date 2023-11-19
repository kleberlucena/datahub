from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa_manager.models import *
from apps.rpa_manager.forms import *
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from base.mixins import GroupRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission
from django.db.models import Q 


MESSAGE_MODEL_NAME = 'Guarnição'


class GuarnicaoCreateView(GroupRequiredMixin, CreateView):
    model = PoliceGroup
    form_class = PoliceGroupForm
    template_name = 'rpa_manager/create_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:checklist_form')
    group_required = ['profile:rpa_basic', "profile:rpa_advanced"]
    
    def form_valid(self, form):
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} cadastrada com sucesso!')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user.military
        kwargs['initial'] = {'remote_pilot': user}
        return kwargs
        
    
class GuarnicaoUpdateView(GroupRequiredMixin, UpdateView):
    model = PoliceGroup
    form_class = PoliceGroupForm
    template_name = 'rpa_manager/update_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:checklist_form')
    group_required = ['profile:rpa_basic', "profile:rpa_advanced"]
    
    def get_object(self, queryset=None):
        return PoliceGroup.objects.latest('date')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        
        return response   
    
class GuarnicaoDeleteView(PermissionRequiredMixin, DeleteView):
    model = PoliceGroup
    # template_name = 'controle/pages/delete_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:painel')
    context_object_name = 'obj'
    permission_required = 'rpa_manager.delete_guarnicao'
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class DescadastrarGuarnicao(GroupRequiredMixin, View):
    template_name = 'rpa_manager/unregister_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:painel')
    group_required = ['profile:rpa_basic', "profile:rpa_advanced"]
    
    def get(self, request, *args, **kwargs):
        user = self.request.user.military
        last_guarnicao = PoliceGroup.objects.filter(remote_pilot=user).order_by('-id').first()
        if last_guarnicao:
            return render(request, self.template_name, {'guarnicao': last_guarnicao})
        return redirect(self.success_url)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user.military
        last_guarnicao = PoliceGroup.objects.filter(remote_pilot=user).order_by('-id').first()
        if last_guarnicao:
            last_guarnicao.delete()
            
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} descadastrada com sucesso!')
        return redirect(self.success_url)
    

