from django.views.generic import DetailView, UpdateView, DeleteView
from apps.rpa_manager.forms import ChecklistForm
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.rpa_manager.utils.saveNewChecklistInAircraftHistoric import saveNewChecklistInAircraftHistoric
from apps.rpa_manager.utils.getLastRegisteredChecklistData import getLastRegisteredChecklistData
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission
from django.contrib import messages
from apps.rpa_manager.models import (Checklist, 
                                     HistoricoAlteracoesAeronave, 
                                     Guarnicao, 
                                     Bateria,ImagensChecklist)


MESSAGE_MODEL_NAME = 'Checklist'

class VerChecklistView(PermissionRequiredMixin, DetailView):
    model = Checklist
    template_name = 'rpa_manager/detail_checklist.html'
    context_object_name = 'checklist'
    permission_required = 'rpa_manager.view_checklist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklist = self.get_object()
        images = ImagensChecklist.objects.filter(checklist=checklist)
        image_urls = [image.imageChecklist.url for image in images]
        
        lista_de_alteracoes = self.object.alteracoes.split('\n')
        nova_lista_alteracoes = []
        for item in lista_de_alteracoes:
            if len(lista_de_alteracoes) == 1 and lista_de_alteracoes[0] == '':
                nova_lista_alteracoes.append('Sem alterações')
            else:
                nova_lista_alteracoes.append(item)
        context['nova_lista_alteracoes'] = nova_lista_alteracoes
        context['image_urls'] = image_urls
        return context

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ChecklistFormView(PermissionRequiredMixin, View):    
    permission_required = 'rpa_manager.add_checklist'
    
    def get(self, request, *args, **kwargs):
        piloto = request.user
        historico_checklist_dict = {}
        
        historico_checklist_dict_json = getLastRegisteredChecklistData(historico_checklist_dict)
        baterias = Bateria.objects.all()
        
        ultima_guarnicao = Guarnicao.objects.filter(piloto_remoto=request.user).latest('data')
        
        dados_checklist = { 'piloto': piloto,
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
            'piloto': request.user,
        }
        
        checklist_form = ChecklistForm(request.POST, initial=dados_checklist)
        
        if checklist_form.is_valid():
            saveNewChecklistInAircraftHistoric(request.POST, dados_checklist)
            checklist = checklist_form.save()
            
            images = self.request.FILES.getlist('imagens')
             # checklist = Checklist.objects.create(piloto=request.user, guarnicao=alguma_guarnicao)
            for image in images:
                ImagensChecklist.objects.create(checklist=checklist, imageChecklist=image)
           
            return redirect('rpa_manager:update_all_batteries')
        
        context = {
            'checklist_form': checklist_form,
        }
        
        return render(request, 'rpa_manager/create_checklist.html', context)
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class EditarChecklistView(PermissionRequiredMixin, UpdateView):
    model = Checklist
    form_class = ChecklistForm
    template_name = 'rpa_manager/update_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    context_object_name = 'form'
    permission_required = 'rpa_manager.change_checklist'
    
    def form_valid(self, form):
        checklist = form.save(commit=False)
        aeronave = checklist.aeronave

        ultimo_checklist = Checklist.objects.filter(aeronave=aeronave).order_by('-data', '-horario').first()
        if checklist == ultimo_checklist:
            historico = HistoricoAlteracoesAeronave.objects.filter(aeronave=aeronave).order_by('-data').first()
            if historico:
                historico.alteracoes = checklist.alteracoes
                historico.num_helices = checklist.num_helices
                historico.num_baterias = checklist.num_baterias
                # Atualize outros campos de histórico, se necessário
                historico.save()
            
        images = self.request.FILES.getlist('imagens')
        for image in images:
            ImagensChecklist.objects.create(checklist=checklist, imageChecklist=image)
                
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editado com sucesso!')
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        checklist = self.get_object()

        images = ImagensChecklist.objects.filter(checklist=checklist)
        
        image_urls = [image.imageChecklist.url for image in images]
        context['image_urls'] = image_urls
        context['images'] = images

        return context
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class DeletarChecklistView(PermissionRequiredMixin, DeleteView):
    model = Checklist
    template_name = 'rpa_manager/delete_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    context_object_name = 'obj'
    permission_required = 'rpa_manager.delete_checklist'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} excluído com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class ChecklistImageDeleteView(DeleteView):
    model = ImagensChecklist
    template_name = 'rpa_manager/delete_image_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    
    def delete(self, request, *args, **kwargs):
        imagem = self.get_object()
        if imagem:
            imagem.delete()
            return JsonResponse({'message': 'Imagem excluída com sucesso.'})
        else:
            return JsonResponse({'error': 'Imagem não encontrada.'}, status=404)