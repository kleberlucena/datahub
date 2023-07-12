
from django.contrib.auth.models import User
from django.shortcuts import render

from apps.rpa_manager.models import (Aeronave, Bateria, 
                                     Checklist, Militar, 
                                     Missao, Relatorio
                                     )
from . views_crud_aeronaves import *
from . views_crud_baterias import *
from . views_crud_checklists import *
from . views_crud_efetivo import *
from . views_crud_missao import *
from . views_crud_relatorio import *
from . views_funcoes_auxiliares import *

from django.views.generic import TemplateView

def home(request):
    return render(request, 'controle/pages/base.html')

class PainelView(TemplateView):
    template_name = 'controle/pages/painel.html'

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
        form = formulario_missao(self.request)

        context['militares'] = militares
        context['form'] = form
        context['numero_de_usuarios'] = numero_de_usuarios

        militares_com_roles = {}
        for militar in militares:
            roles = militar.roles.all()
            militares_com_roles[militar] = roles

        context['militares_com_roles'] = militares_com_roles
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
    