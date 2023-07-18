from django.views.generic import DetailView, UpdateView, DeleteView
from apps.rpa_manager.forms import ChecklistForm, Aeronave
from apps.rpa_manager.models import Checklist, HistoricoAlteracoesAeronave
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
import json

from .utils.getLastRegistedChecklistData import getLastRegistedChecklistData

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

        getLastRegistedChecklistData(historico_checklist_dict)
       
        historico_checklist_dict_json = json.dumps(historico_checklist_dict)
        
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
            checklist = checklist_form.save()
            
            # Salvar as informações no histórico de alterações
            HistoricoAlteracoesAeronave.objects.create(
                aeronave=checklist.aeronave,
                num_helices = checklist.num_helices,  
                num_baterias = checklist.num_baterias, 
                baterias_carregadas = checklist.baterias_carregadas, 
                bateria_controle_carregada = checklist.bateria_controle_carregada, 
                corpo = checklist.corpo, 
                hastes_motor = checklist.hastes_motor, 
                helices = checklist.helices, 
                gimbal = checklist.gimbal, 
                holofote = checklist.holofote, 
                auto_falante = checklist.auto_falante, 
                luz_estroboscopica= checklist.luz_estroboscopica, 
                cabos = checklist.cabos, 
                carregador = checklist.carregador, 
                fonte = checklist.fonte, 
                smart_controller = checklist.smart_controller, 
                controle = checklist.controle, 
                cartao_sd = checklist.cartao_sd, 
                IMU = checklist.IMU, 
                compass = checklist.compass, 
                sinal_transmissao = checklist.sinal_transmissao, 
                sistema_rtk_ppk = checklist.sistema_rtk_ppk, 
                sinal_de_video = checklist.sinal_de_video, 
                telemetria = checklist.telemetria, 
                paraquedas = checklist.paraquedas,                
                alteracoes = checklist.alteracoes
            )
            
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context["edicao_checklist"] = True
        return context
    

class DeletarChecklistView(DeleteView):
    model = Checklist
    template_name = 'controle/pages/delete_checklist.html'
    success_url = reverse_lazy('rpa_manager:checklists')
    context_object_name = 'obj'
