from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa.forms import *
from apps.rpa.models import *
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from base.mixins import GroupRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from apps.rpa.handlers import require_permission

MESSAGE_MODEL_NAME = 'Bateria'


class VerBateriaView(GroupRequiredMixin, DetailView):
    model = Battery
    template_name = 'rpa/detail_battery.html'
    context_object_name = 'bateria'
    pk_url_kwarg = 'pk'
    group_required = ['profile:rpa_advanced']

    
class CriarNovaBateriaView(GroupRequiredMixin, CreateView):
    model = Battery
    form_class = BatteryForm
    template_name = 'rpa/create_battery.html'
    success_url = reverse_lazy('rpa:baterias')
    group_required = ['profile:rpa_advanced']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criada com sucesso!')
        return response

    
class EditarBateriaView(GroupRequiredMixin, UpdateView):
    model = Battery
    form_class = BatteryForm
    template_name = 'rpa/update_battery.html'
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa:baterias')
    group_required = ['profile:rpa_advanced']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
        return response

    
class DeletarBateriaView(GroupRequiredMixin, DeleteView):
    model = Battery
    template_name = 'rpa/delete_battery.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa:baterias')
    group_required = ['profile:rpa_advanced']
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
        return response
    
    
    
class UpdateAllBateriasView(View):
    template_name = 'rpa/update_all_batteries.html'

    def get(self, request):
        baterias = Battery.objects.all()
        return render(request, self.template_name, {'baterias': baterias})

    def post(self, request):
        for bateria_id, num_cicles in request.POST.items():
            if bateria_id.isdigit():
                bateria = Battery.objects.get(id=int(bateria_id))
                bateria.num_cicles = int(num_cicles)
                bateria.save()

        messages.success(self.request, f'Checklist criado com sucesso!')
        
        return redirect('rpa:painel')
