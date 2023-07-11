
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from apps.rpa_manager.models import Aeronave, Bateria, Checklist, Militar, Missao, Relatorio
from . views_cards import cards
from . views_crud_aeronaves import *
from . views_crud_baterias import *
from . views_crud_checklists import *
from . views_crud_efetivo import *
from . views_crud_missao import *
from . views_crud_relatorio import *
from . views_dashboard_cards import dashboard_cards
from . views_funcoes_auxiliares import *

from django.views.generic import TemplateView

def home(request):
    return render(request, 'controle/pages/base.html')

class PainelView(TemplateView):
    template_name = 'controle/pages/painel.html'

def dashboard(request):
    numero_de_missoes = obtem_total_de_missoes()
    missoes_por_mes = obtem_numero_de_missoes_por_mes()
    opm_maior_apoio, numero_opm_maior_apoio = obtem_total_de_opms_apioadas()
    unidade_maior_apoio, numero_unidade_maior_apoio = obtem_total_de_unidades_apioadas()
    local_maior_apoio, numero_local_maior_apoio = obtem_localidade_com_maior_apoio()
    
    context = {
        'numero_de_missoes': numero_de_missoes,
        'missoes_por_mes': missoes_por_mes,
        'opm_maior_apoio': opm_maior_apoio,
        'numero_opm_maior_apoio': numero_opm_maior_apoio,
        'unidade_maior_apoio': unidade_maior_apoio,
        'numero_unidade_maior_apoio': numero_unidade_maior_apoio,
        'local_maior_apoio': local_maior_apoio,
        'numero_local_maior_apoio': numero_local_maior_apoio,
        'dashboard_cards' : dashboard_cards,
    }
    
    return render(request, 'controle/pages/dashboard.html', context)

def obtem_dados_de_missoes_por_mes(request):
    missoes_por_mes = obtem_numero_de_missoes_por_mes()
    
    return JsonResponse(missoes_por_mes, safe=False)

def obtem_dados_de_missoes_por_usuario(request):
    missoes_por_usuario = numero_de_missoes_por_usuario()
    usuariosPorMissoes = {}
    
    for usuario in missoes_por_usuario:
        new_key = str(User.objects.get(pk=usuario)) 
        value = missoes_por_usuario[usuario]
        usuariosPorMissoes[new_key] = value
        
    return JsonResponse(usuariosPorMissoes, safe=False)
    
class PrincipalView(TemplateView):
    template_name = 'controle/pages/tela_principal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        missoes = Missao.objects.all().order_by('-data', '-horario')
        form = formulario_missao(self.request)

        context['missoes'] = missoes
        context['form'] = form

        return context

class ChecklistsView(TemplateView):
    template_name = 'controle/pages/checklists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklists = Checklist.objects.all().order_by('-data', '-horario')
        form = formulario_missao(self.request)

        context['checklists'] = checklists
        context['form'] = form

        return context


class RelatoriosView(TemplateView):
    template_name = 'controle/pages/relatorios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relatorios = Relatorio.objects.all().order_by('-horario_inicial', '-data')
        form = formulario_missao(self.request)

        context['relatorios'] = relatorios
        context['form'] = form

        return context


class EfetivoView(TemplateView):
    template_name = 'controle/pages/usuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        militares = Militar.objects.all()
        numero_de_usuarios = User.objects.count()
        missoes_por_usuario = numero_de_missoes_por_usuario()
        form = formulario_missao(self.request)

        context['militares'] = militares
        context['form'] = form
        context['missoes_por_usuario'] = missoes_por_usuario
        context['numero_de_usuarios'] = numero_de_usuarios

        return context


class AeronavesView(TemplateView):
    template_name = 'controle/pages/aeronaves.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aeronaves = Aeronave.objects.all()
        form = formulario_missao(self.request)

        context['aeronaves'] = aeronaves
        context['form'] = form

        return context


# def baterias(request):
#     limite_de_ciclos = 45 
    
#     baterias = Bateria.objects.all()
    
#     ids_baterias_nivel_critico = baterias_em_nivel_critico(limite_de_ciclos)

#     form = formulario_missao(request)
 
#     context = { 
#                 'baterias': baterias,
#                 'ids_baterias_nivel_critico': ids_baterias_nivel_critico, 
#                 'form': form,
#             }
#     return render(request, 'controle/pages/baterias.html', context)

class BateriasView(TemplateView):
    template_name = 'controle/pages/baterias.html'
    limite_de_ciclos = 45
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baterias = Bateria.objects.all()
        ids_baterias_nivel_critico = baterias_em_nivel_critico(self.limite_de_ciclos)
        form = formulario_missao(self.request)

        context['baterias'] = baterias
        context['ids_baterias_nivel_critico'] = ids_baterias_nivel_critico
        context['form'] = form

        return context

def retorna_total_de_missoes(request):
    total_de_missoes = Missao.objects.count()
    
    return JsonResponse({'total_de_missoes': total_de_missoes})
