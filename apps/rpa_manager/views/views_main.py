
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .views_crud_aeronaves import *
from .views_crud_baterias import *
from .views_crud_checklists import *
from .views_crud_efetivo import *
from .views_crud_missao import *
from .views_crud_relatorio import *
from .views_funcoes_auxiliares import *
from apps.rpa_manager.forms import AeronaveSelectForm
from apps.rpa_manager.utils.create_json_for_coordinates import create_json_for_coordinates
from apps.rpa_manager.models import (Aeronave, Bateria, 
                                     Checklist, Militar, 
                                     Missao, Relatorio,
                                     HistoricoAlteracoesAeronave
                                     )


def home(request):
    return render(request, 'controle/pages/base.html')


class PainelView(TemplateView):
    template_name = 'controle/pages/painel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coordinates_dict = {}
        ultimo_relatorio = Relatorio.objects.latest('id')
        coordinates_json = create_json_for_coordinates(coordinates_dict, ultimo_relatorio)
        context['coordinates_json'] = coordinates_json

        return context


class PrincipalView(TemplateView):
    template_name = 'controle/pages/operacoes.html'

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
        relatorios = Relatorio.objects.all().order_by('-data', '-horario_inicial', )
        print(relatorios)
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


class HistoricosPorAeronaveView(ListView):
    model = HistoricoAlteracoesAeronave
    template_name = 'controle/pages/aircraft_historic.html'
    context_object_name = 'aircraft_historic'
    form_class = AeronaveSelectForm

    def get_queryset(self):
        queryset = super().get_queryset()
        aeronave_id = self.request.GET.get('aeronave')
        if aeronave_id:
            queryset = queryset.filter(aeronave__id=aeronave_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET or None)
        return context