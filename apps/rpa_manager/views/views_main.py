from typing import List, Dict
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
        coordinates_dict: Dict = {}
        report_by_date_list: List = []
        lista_de_guarnicoes = []
        
        ultimo_relatorio = Relatorio.objects.latest('id')
        default_month: int = 1
        default_year: int = 2023
        month: int = int(self.request.GET.get('month', default_month))  
        year: int = int(self.request.GET.get('year', default_year))  
        
        report_by_date = Relatorio.objects.filter(data__month=month, data__year=year)
        for report in report_by_date:
            report_by_date_list.append({
                'usuario': report.militar.username,
                'titulo': report.titulo,
                'latitude': report.latitude,
                'longitude': report.longitude
                })
        
        
        localidades = CidadesPB.objects.all()
        for local in localidades:
            # data__date=date.today()
            guarnicoes = Guarnicao.objects.filter(local=local)
            for guarnicao in guarnicoes:
                lista_de_guarnicoes.append({
                    'id': guarnicao.id,
                    'motorista': guarnicao.motorista,
                    'piloto_remoto': guarnicao.piloto_remoto.username,
                    'piloto_observador': guarnicao.piloto_observador.nome_de_guerra,
                    'local': guarnicao.local.cidades_pb,
                    'telefone': guarnicao.telefone,
                })
                
        guarnicoes_json = json.dumps(lista_de_guarnicoes, indent=4, ensure_ascii=False)
       
        coordinates_by_date_json = json.dumps(report_by_date_list, indent=4)
        coordinates_json = create_json_for_coordinates(coordinates_dict, ultimo_relatorio)
        print(coordinates_json)
        context['coordinates_json'] = coordinates_json
        context['coordinates_by_date_json'] = coordinates_by_date_json
        context['guarnicoes_json'] = guarnicoes_json
        return context


class PrincipalView(LoginRequiredMixin, TemplateView):
    template_name = 'controle/pages/operacoes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = formulario_missao(self.request)

        # Verifica se o usuário é um superuser
        if self.request.user.is_superuser:
            missoes = Missao.objects.all().order_by('-data', '-horario')
        else:
            # Filtra os objetos para exibir apenas os que foram criados pelo usuário atual
            missoes = Missao.objects.filter(usuario=self.request.user).order_by('-data', '-horario')

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
        
        relatorios = Relatorio.objects.all().order_by('-data', 'horario_inicial')

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