from django.views.generic import DetailView, UpdateView, DeleteView
from apps.rpa_manager.forms import *
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.rpa_manager.utils.saveNewChecklistInAircraftHistoric import saveNewChecklistInAircraftHistoric
from apps.rpa_manager.utils.getLastRegisteredChecklistData import getLastRegisteredChecklistData
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from base.mixins import GroupRequiredMixin
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission
from django.contrib import messages
from apps.rpa_manager.models import *


MESSAGE_MODEL_NAME = 'Checklist'

class VerChecklistView(GroupRequiredMixin, DetailView):
    model = Checklist
    template_name = 'rpa_manager/detail_checklist.html'
    context_object_name = 'checklist'
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklist = self.get_object()
        images = ChecklistImages.objects.filter(checklist=checklist)
        image_urls = [image.imageChecklist.url for image in images]
        
        lista_de_alteracoes = self.object.changes.split('\n')
        nova_lista_alteracoes = []
        for item in lista_de_alteracoes:
            if len(lista_de_alteracoes) == 1 and lista_de_alteracoes[0] == '':
                nova_lista_alteracoes.append('Sem alterações')
            else:
                nova_lista_alteracoes.append(item)
        context['nova_lista_alteracoes'] = nova_lista_alteracoes
        context['image_urls'] = image_urls
        return context


class ChecklistFormView(GroupRequiredMixin, View):    
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get(self, request, *args, **kwargs):
        remote_pilot = request.user
        historico_checklist_dict = {}
        
        historico_checklist_dict_json = getLastRegisteredChecklistData(historico_checklist_dict)
        baterias = Battery.objects.all()       
        
        
        try:
            ultima_guarnicao = PoliceGroup.objects.filter(remote_pilot=request.user.military).latest('date')
            print(ultima_guarnicao)
        except:
            ultima_guarnicao = None
            
        dados_checklist = { 'remote_pilot': remote_pilot,
                           'guarnicao': ultima_guarnicao, }
            
        checklist_form = ChecklistForm(initial=dados_checklist)
        context = {
            'checklist_form': checklist_form,
            'historico_checklist_dict_json': historico_checklist_dict_json,
            'guarnicao': ultima_guarnicao,
            'baterias': baterias
            }
        return render(request, 'rpa_manager/create_checklist.html', context)
    
    def post(self, request):
        
        dados_checklist = {
            'remote_pilot': request.user,
        }
        
        checklist_form = ChecklistForm(request.POST, initial=dados_checklist)
        
        if checklist_form.is_valid():
            saveNewChecklistInAircraftHistoric(request.POST, dados_checklist)
            checklist = checklist_form.save()
            
            images = self.request.FILES.getlist('imagens')
             
            for image in images:
                ChecklistImages.objects.create(checklist=checklist, imageChecklist=image)
           
            return redirect('rpa_manager:update_all_batteries')
        
        context = {
            'checklist_form': checklist_form,
        }
        
        return render(request, 'rpa_manager/create_checklist.html', context)
    
class EditarChecklistView(GroupRequiredMixin, UpdateView):
    model = Checklist
    form_class = ChecklistForm
    template_name = 'rpa_manager/update_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    context_object_name = 'form'
    group_required = ['profile:rpa_advanced']
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        checklist = self.get_object()
        
        images = ChecklistImages.objects.filter(checklist=checklist)
        image_urls = [image.imageChecklist.url for image in images]
        context['image_urls'] = image_urls
        context['images'] = images
        
        return context
    
    def form_valid(self, form):
        obj = self.get_object()
        checklist = form.save(commit=False)
        
        new_aircraft = form.cleaned_data['aircraft']
        if new_aircraft != obj.aircraft:
            messages.error(self.request, 'Você não pode mudar a aeronave durante a edição.')
            return self.form_invalid(form)
        
        aircraft = checklist.aircraft
        ultimo_checklist = Checklist.objects.filter(aircraft=aircraft).order_by('-date', '-time').first()
        if checklist == ultimo_checklist:
            historico = AicraftHistoric.objects.filter(aircraft=aircraft).order_by('-date').first()
            if historico:
                historico.changes = checklist.changes
                historico.num_propellers = checklist.num_propellers
                historico.num_batteries = checklist.num_batteries
                historico.save()
            
        images = self.request.FILES.getlist('imagens')
        for image in images:
            ChecklistImages.objects.create(checklist=checklist, imageChecklist=image)
                
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editado com sucesso!')
        
        return super().form_valid(form)
    
class DeletarChecklistView(PermissionRequiredMixin, DeleteView):
    model = Checklist
    template_name = 'rpa_manager/delete_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    context_object_name = 'obj'
    permission_required = 'rpa_manager.delete_checklist'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluído com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class ChecklistImageDeleteView(DeleteView):
    model = ChecklistImages
    template_name = 'rpa_manager/delete_image_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    
    def delete(self, request, *args, **kwargs):
        imagem = self.get_object()
        if imagem:
            imagem.delete()
            return JsonResponse({'message': 'Imagem excluída com sucesso.'})
        else:
            return JsonResponse({'error': 'Imagem não encontrada.'}, status=404)