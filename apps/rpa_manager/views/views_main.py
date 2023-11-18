from typing import List, Dict
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView
from base.mixins import GroupRequiredMixin
from .views_crud_aeronaves import *
from .views_crud_baterias import *
from .views_crud_checklists import *
from .views_crud_missao import *
from .views_crud_relatorio import *
from .views_funcoes_auxiliares import *
from apps.rpa_manager.forms import AircraftSelectionForm, TypeOfBatteryForm
from apps.rpa_manager.utils.createJsonByLastOperation import createJsonByLastOperation
from apps.rpa_manager.utils.getTodayLatLonCoordinates import getTodaysCoordinates
from apps.rpa_manager.utils.getOperationInCourse import getOperationInCourse

from apps.rpa_manager.utils.rpaManagerDashboard import *
from apps.portal.models import *
from apps.rpa_manager.models import *
from datetime import datetime

def home(request):
    return render(request, 'rpa_manager/base.html')

class DashboardRpaManager(TemplateView):
    template_name = 'rpa_manager/dashboard_rpamanager.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        rpa_dashboard = RpaManagerDashboard()
        chart_data = rpa_dashboard.get_chart_data()
        context['amount_of_operations'] = rpa_dashboard.get_amount_of_operations
        context['pilot_with_max_operations'] = rpa_dashboard.get_pilot_with_max_operations
        context['number_of_pilot_max_oper'] = rpa_dashboard.get_number_of_pilot_max_oper
        context['most_supported_location'] = rpa_dashboard.get_most_supported_location()
        context['operations_in_course'] = rpa_dashboard.get_operations_in_course()
        context['available_aircrafts'] = rpa_dashboard.get_available_aircrafts()
        context['most_used_aircraft'] = rpa_dashboard.get_most_used_aircraft()
        context['battery_info'] = rpa_dashboard.get_batteries_cicles_level()
        context['chart_data'] = chart_data
        
        return context

class PainelView(TemplateView):
    template_name = 'rpa_manager/painel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_coordinates_operations = getTodaysCoordinates(context)
        operationsInCourseJson = getOperationInCourse()
        coordinates_dict: Dict = {}
        report_by_date_list: List = []
        lista_de_guarnicoes = []

        year = datetime.now().year
        years = []
        for i in range(year-8, year+1, 1):
            years.append(i)
        years = years[::-1]
        
        default_month: int = 1
        default_year: int = 2023
        month: int = int(self.request.GET.get('month', default_month))  
        year: int = int(self.request.GET.get('year', default_year))  
        
        report_by_date = Report.objects.filter(date__month=month, date__year=year)
        for report in report_by_date:
            report_by_date_list.append({
                'usuario': report.remote_pilot.military.nickname,
                'titulo': report.title,
                'latitude': report.latitude,
                'longitude': report.longitude
                })
        
        localidades = CitiesPB.objects.all()
        for local in localidades:
            guarnicoes = PoliceGroup.objects.filter(location=local)

            for guarnicao in guarnicoes:
                lista_de_guarnicoes.append({
                    'id':  
                        guarnicao.id if(guarnicao.id != None) else 'sem registro',
                    'motorista': 
                        str(guarnicao.driver) if(guarnicao.driver != None) else 'sem registro',
                    'motorista_img': 
                        str(guarnicao.driver.image.url) if(guarnicao.driver != None) else 'sem registro',
                    'piloto_remoto': 
                        str(guarnicao.remote_pilot) if(guarnicao.remote_pilot != None) else 'sem registro',
                    'piloto_remoto_img': 
                        str(guarnicao.remote_pilot.image.url) if(guarnicao.remote_pilot != None) else 'sem registro',
                    'piloto_observador': 
                        str(guarnicao.observer_pilot) 
                        if(guarnicao.observer_pilot != None) else 'sem registro',
                    'piloto_observador_img': 
                        str(guarnicao.observer_pilot.image.url) 
                        if(guarnicao.observer_pilot != None) else 'sem registro',
                    'local': 
                        guarnicao.location.cities_pb if(guarnicao.location.cities_pb != None) else 'sem registro',
                    'telefone': 
                        guarnicao.phone if(guarnicao.id != None) else 'sem registro',
                })
                
        guarnicoes_json = json.dumps(lista_de_guarnicoes, indent=4, ensure_ascii=False)
       
        coordinates_by_date_json = json.dumps(report_by_date_list, indent=4)
        
        try:
            ultima_operacao = Operation.objects.latest('id')
        except ObjectDoesNotExist:
            ultima_operacao = None
        
        coordinates_json = createJsonByLastOperation(coordinates_dict, ultima_operacao)
        context['coordinates_json'] = coordinates_json
        context['coordinates_by_date_json'] = coordinates_by_date_json
        context['today_coordinates_operations'] = today_coordinates_operations
        context['operationsInCourse'] = operationsInCourseJson
        context['guarnicoes_json'] = guarnicoes_json
        context['years'] = years

        rpa_dashboard = RpaManagerDashboard()
        context['operations_in_course'] = rpa_dashboard.get_operations_in_course()
        return context


class PrincipalView(GroupRequiredMixin, TemplateView):
    template_name = 'rpa_manager/list_operations.html'
    group_required = ['profile:rpa_view', 'profile:rpa_basic', 'profile:rpa_advanced']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = formulario_missao(self.request)

        user = self.request.user
        
        if user.is_superuser or user.groups.filter(name='profile:rpa_view').exists():
            missoes = Operation.objects.all().order_by('-date', '-time')
        else:
            missoes = Operation.objects.filter(user=self.request.user).order_by('-date', '-time')

        context['missoes'] = missoes
        context['form'] = form

        return context


class PointsOfInterestView(GroupRequiredMixin, TemplateView):
    model = PointsOfInterest
    context_object_name = 'points_of_interest'
    template_name = 'rpa_manager/list_points_of_interests.html'
    group_required = ['profile:rpa_view', 'profile:rpa_basic', 'profile:rpa_advanced']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["points_of_interest"] = PointsOfInterest.objects.all()
        return context


class ChecklistsView(GroupRequiredMixin, TemplateView):
    template_name = 'rpa_manager/list_checklists.html'
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='profile:rpa_view').exists():
            checklists = Checklist.objects.all().order_by('-date', '-time')
        else:
            checklists = Checklist.objects.filter(remote_pilot=user).order_by('-date', '-time')

        form = formulario_missao(self.request)

        context['checklists'] = checklists
        context['form'] = form

        return context


class RelatoriosView(GroupRequiredMixin, TemplateView):
    template_name = 'rpa_manager/list_reports.html'
    group_required = ['profile:rpa_view', 'profile:rpa_basic','profile:rpa_advanced']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relatorios = Report.objects.all().order_by('-date', '-initial_time')

        form = formulario_missao(self.request)

        context['relatorios'] = relatorios
        context['form'] = form

        return context


class IncidentesView(GroupRequiredMixin, TemplateView):
    template_name = 'rpa_manager/list_incidents.html'
    group_required = ['profile:rpa_basic','profile:rpa_advanced']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='profile:rpa_view').exists():
            incidentes = Incidents.objects.all().order_by('-date')
        else:
            incidentes = Incidents.objects.filter(remote_pilot=self.request.user).order_by('-date')
        context['incidentes'] = incidentes
        
        return context


class AeronavesView(GroupRequiredMixin, TemplateView):
    template_name = 'rpa_manager/list_aircrafts.html'
    group_required = ['profile:rpa_advanced']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aeronaves = Aircraft.objects.all()
        form = formulario_missao(self.request)

        context['aeronaves'] = aeronaves
        context['form'] = form

        return context
    

class BateriasView(GroupRequiredMixin, TemplateView):
    template_name = 'rpa_manager/list_batteries.html'
    group_required = ['profile:rpa_advanced']
    limite_de_ciclos = 45
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baterias = Battery.objects.all()
        ids_baterias_nivel_critico = baterias_em_nivel_critico(self.limite_de_ciclos)
        form = formulario_missao(self.request)

        context['baterias'] = baterias
        context['ids_baterias_nivel_critico'] = ids_baterias_nivel_critico
        context['form'] = form

        return context


class HistoricosPorAeronaveView(GroupRequiredMixin, ListView):
    model = AicraftHistoric
    template_name = 'rpa_manager/list_aircraft_historic.html'
    context_object_name = 'aircraft_historic'
    form_class = AircraftSelectionForm
    group_required = ['profile:rpa_advanced']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        aeronave_id = self.request.GET.get('aircraft')
        if aeronave_id:
            queryset = queryset.filter(aircraft__id=aeronave_id).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET or None)
        return context
    
    
class LegislationsView(ListView):
    model = Legislation
    template_name = 'rpa_manager/list_of_legislation.html'
    context_object_name = 'legislations'
    
    
class TypeOfBatteryView(TemplateView):
    template_name = 'rpa_manager/list_types_of_batteries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_of_batteries = TypeOfBattery.objects.all()
        form = TypeOfBatteryForm(self.request)

        context['type_of_batteries'] = type_of_batteries
        context['form'] = form

        return context
