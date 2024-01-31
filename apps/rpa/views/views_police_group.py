from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from base.mixins import GroupRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Q 

from apps.rpa.handlers import require_permission
from apps.rpa.models import *
from apps.rpa.forms import *
from apps.rpa.forms.forms_police_group import PoliceGroupForm2


MESSAGE_MODEL_NAME = 'Guarnição'


class PoliceGroupCreateView(GroupRequiredMixin, CreateView):
    model = PoliceGroup
    form_class = PoliceGroupForm2
    template_name = 'rpa/police_group/create.html'
    success_url = reverse_lazy('rpa:checklist_form')
    group_required = ['profile:rpa_basic', "profile:rpa_advanced"]
    
    def form_valid(self, form):
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} cadastrada com sucesso!')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'remote_pilot': self.request.user.military}
        return kwargs
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # existing_guarnicao = PoliceGroup.objects.filter(
        #     Q(remote_pilot=request.user.military) | Q(observer_pilot=request.user.military) | Q(driver=request.user.military)
        # ).first()

        # if existing_guarnicao:
        #     messages.info(self.request, 'O usuário logado já participa de uma guarnição')
        #     return redirect('rpa:painel')
        
        return super().get(request, *args, **kwargs)
        
    
class PoliceGroupUpdateView(GroupRequiredMixin, UpdateView):
    model = PoliceGroup
    form_class = PoliceGroupForm
    template_name = 'rpa/police_group/update.html'
    success_url = reverse_lazy('rpa:checklist_form')
    group_required = ['profile:rpa_basic', "profile:rpa_advanced"]
    
    # def get_object(self, queryset=None):
    #     return PoliceGroup.objects.get(id=self.request.content_params('pk'))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        
        return response   
    
class PoliceGroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = PoliceGroup
    # template_name = 'controle/pages/delete_guarnicao.html'
    success_url = reverse_lazy('rpa:painel')
    context_object_name = 'obj'
    permission_required = 'rpa.delete_guarnicao'
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class PoliceGroupArchiveView(GroupRequiredMixin, View):
    template_name = 'rpa/unregister_police_group.html'
    success_url = reverse_lazy('rpa:painel')
    group_required = ['profile:rpa_basic', "profile:rpa_advanced"]
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        military = self.request.user.military
        last_guarnicao = PoliceGroup.objects.filter(remote_pilot=military).order_by('-id').first()
        if last_guarnicao:
            return render(request, self.template_name, {'guarnicao': last_guarnicao})
        return redirect(self.success_url)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        military = self.request.user.military
        last_guarnicao = PoliceGroup.objects.filter(remote_pilot=military).order_by('-id').first()
        if last_guarnicao:
            last_guarnicao.delete()
            
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} descadastrada com sucesso!')
        return redirect(self.success_url)
    
   
# Retorna um input de busca de militares
def military_search(request):
    template_name = 'rpa/police_group/military_search.html'

    return render(request, template_name)

# Retorna um modal
def modal(request):
    template_name = 'rpa/police_group/modal.html'

    return render(request, template_name)

# Retorna uma lista de options para o select de militares
def militaries(request):
    template_name = 'rpa/police_group/militaries_list.html'
    term = request.GET.get('term')

    militaries = Military.objects.filter(register__icontains=term).values()[:10]

    context = {'militaries': militaries}
    return render(request, template_name, context)

