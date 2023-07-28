from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa_manager.models import Guarnicao
from apps.rpa_manager.forms import GuarnicaoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime, date

class GuarnicaoCreateView(CreateView):
    model = Guarnicao
    form_class = GuarnicaoForm
    template_name = 'controle/pages/guarnicao_register.html'
    success_url = reverse_lazy('rpa_manager:checklist_form')
    
    def form_valid(self, form):
        # Verificar se já existe uma guarnição para o usuário logado no mesmo dia
        user = self.request.user
        guarnicoes_no_dia = Guarnicao.objects.filter(piloto_remoto=user)
        
        if guarnicoes_no_dia.exists():
            form.add_error(None, 'Já existe uma guarnição criada por este usuário no mesmo dia.')
            return self.form_invalid(form)

        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'piloto_remoto': self.request.user}
        return kwargs
    
    
class GuarnicaoUpdateView(UpdateView):
    model = Guarnicao
    form_class = GuarnicaoForm
    template_name = 'controle/pages/guarnicao_edit.html' 
    success_url = reverse_lazy('rpa_manager:checklist_form')

    def get_object(self, queryset=None):
        return Guarnicao.objects.latest('data')


class GuarnicaoDeleteView(DeleteView):
    model = Guarnicao
    template_name = 'controle/pages/delete_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:painel')
    context_object_name = 'obj'
    
    
class DescadastrarGuarnicao(LoginRequiredMixin, View):
    template_name = 'controle/pages/descadastrar_guarnicao.html'
    success_url = reverse_lazy('rpa_manager:painel')

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
        return redirect(self.success_url)