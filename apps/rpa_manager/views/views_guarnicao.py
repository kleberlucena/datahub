from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa_manager.models import Guarnicao
from apps.rpa_manager.forms import GuarnicaoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission

MESSAGE_MODEL_NAME = 'Guarnição'


class GuarnicaoCreateView(PermissionRequiredMixin, CreateView):
    model = Guarnicao
    form_class = GuarnicaoForm
    template_name = 'controle/pages/guarnicao_register.html'
    success_url = reverse_lazy('rpa_manager:checklist_form')
    permission_required = 'rpa_manager.add_guarnicao'
    
    def form_valid(self, form):
        user = self.request.user
        guarnicoes_no_dia = Guarnicao.objects.filter(piloto_remoto=user)
        
        if guarnicoes_no_dia.exists():
            form.add_error(None, 'Já existe uma guarnição cadastrada por este usuário no mesmo dia.')
            return self.form_invalid(form)
        
        piloto_observador = form.cleaned_data.get('piloto_observador')
        if piloto_observador:
            guarnicoes_com_piloto = Guarnicao.objects.filter(piloto_observador=piloto_observador)
            if guarnicoes_com_piloto.exists():
                form.add_error('piloto_observador', 'Este piloto observador já foi cadastrado em outra guarnição.')
                return self.form_invalid(form)

        messages.success(self.request, f'{MESSAGE_MODEL_NAME} cadastrada com sucesso!')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'piloto_remoto': self.request.user}
        return kwargs
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class GuarnicaoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Guarnicao
    form_class = GuarnicaoForm
    template_name = 'controle/pages/guarnicao_edit.html' 
    success_url = reverse_lazy('rpa_manager:checklist_form')
    permission_required = 'rpa_manager.change_guarnicao'
    
    def get_object(self, queryset=None):
        return Guarnicao.objects.latest('data')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        
        return response

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class GuarnicaoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Guarnicao
    template_name = 'controle/pages/delete_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:painel')
    context_object_name = 'obj'
    permission_required = 'rpa_manager.delete_guarnicao'
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class DescadastrarGuarnicao(PermissionRequiredMixin, View):
    template_name = 'controle/pages/descadastrar_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:painel')
    permission_required = 'rpa_manager.delete_guarnicao'
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        last_guarnicao = Guarnicao.objects.filter(piloto_remoto=user).order_by('-id').first()
        if last_guarnicao:
            return render(request, self.template_name, {'guarnicao': last_guarnicao})
        return redirect(self.success_url)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        last_guarnicao = Guarnicao.objects.filter(piloto_remoto=user).order_by('-id').first()
        if last_guarnicao:
            last_guarnicao.delete()
            
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} descadastrada com sucesso!')
        return redirect(self.success_url)
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)