from django.views.generic import DetailView, UpdateView, DeleteView
from apps.rpa_manager.forms import ChecklistForm, Aeronave
from apps.rpa_manager.models import Checklist, HistoricoAlteracoesAeronave
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
import json
from django.http import HttpResponseRedirect
from .utils.saveNewChecklistInAircraftHistoric import saveNewChecklistInAircraftHistoric
from .utils.getLastRegisteredChecklistData import getLastRegisteredChecklistData

class VerChecklistView(DetailView):
    model = Checklist
    template_name = 'controle/pages/ver_checklist.html'
    context_object_name = 'checklist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_de_alteracoes = self.object.alteracoes.split('\n')
        nova_lista_alteracoes = []
        for item in lista_de_alteracoes:
            if len(lista_de_alteracoes) == 1 and lista_de_alteracoes[0] == '':
                nova_lista_alteracoes.append('Sem alterações')
            else:
                nova_lista_alteracoes.append(item)
        context['nova_lista_alteracoes'] = nova_lista_alteracoes
        return context


class ChecklistFormView(View):    
    def get(self, request):
        piloto = request.user
        historico_checklist_dict = {}

        historico_checklist_dict_json = getLastRegisteredChecklistData(historico_checklist_dict)
        
        dados_checklist = {
            'piloto': piloto,
        }
            
        checklist_form = ChecklistForm(initial=dados_checklist)
        context = {
            'checklist_form': checklist_form,
            'historico_checklist_dict_json': historico_checklist_dict_json
            }
        return render(request, 'controle/pages/checklist_form.html', context)
    
    def post(self, request):
        dados_checklist = {
            'piloto': request.user,
        }
        
        checklist_form = ChecklistForm(request.POST, initial=dados_checklist)
        if checklist_form.is_valid():
            
            saveNewChecklistInAircraftHistoric(request.POST, dados_checklist)
            
            return redirect('rpa_manager:checklists')
        
        context = {
            'checklist_form': checklist_form,
        }
        return render(request, 'controle/pages/checklist_form.html', context)


class EditarChecklistView(UpdateView):
    model = Checklist
    form_class = ChecklistForm
    template_name = 'controle/pages/editar_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    context_object_name = 'form'
    
    def form_valid(self, form):
        checklist = form.save(commit=False)
        aeronave = checklist.aeronave

        # Verificar se o checklist atual é o mais recente para a aeronave associada
        ultimo_checklist = Checklist.objects.filter(aeronave=aeronave).order_by('-data', '-horario').first()
        if checklist == ultimo_checklist:
            # Atualizar o objeto de histórico mais recente relacionado à aeronave
            historico = HistoricoAlteracoesAeronave.objects.filter(aeronave=aeronave).order_by('-data').first()
            if historico:
                historico.alteracoes = checklist.alteracoes
                historico.num_helices = checklist.num_helices
                historico.num_baterias = checklist.num_baterias
                # Atualize outros campos de histórico, se necessário
                historico.save()

        return super().form_valid(form)

class DeletarChecklistView(DeleteView):
    model = Checklist
    template_name = 'controle/pages/delete_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    context_object_name = 'obj'
