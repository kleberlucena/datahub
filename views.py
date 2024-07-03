from xml.etree.ElementTree import tostring
from django.db import transaction
from django.db.models import F
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Incident, Local, Vehicles, Guns, Money, Drug, Arrestings, OccurrenceNature, OccurrenceNaturelist
from .forms import IncidentForm, LocalForm, ArrestingsForm, VehiclesForm, GunsForm, MoneyForm, DrugForm, OcurrencenatureForm
from .forms import ArrestingsFormSet, LocalFormSet, GunsFormSet, VehiclesFormSet, DrugFormSet, MoneyFormSet, OcurrencenatureFormSet
from django.forms import modelformset_factory
from django.views.generic.edit import UpdateView
from django.conf import settings


class IndexView(TemplateView):
    template_name = "datahub/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidents'] = Incident.objects.all()
        return context

class formocorrenciaView(TemplateView):
    template_name = "datahub/formocorrencia.html"

class formocorr_detalheView(TemplateView):
    template_name = "datahub/formocorr_detalhe.html"

class ocorrenciasView(TemplateView):
    template_name = "datahub/ocorrencias.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Consulta o banco de dados para obter todas as instâncias de Incident
        incidents = Incident.objects.all()
        # Adiciona a variável incidents ao contexto
        context['incidents'] = incidents
        return context

class analiseView(TemplateView):
    template_name = "datahub/analise.html"

class analise_detalheView(TemplateView):
    template_name = "datahub/analise_detalhe.html"

class create_incidentView(CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'datahub/formocorrenciacad.html'
    success_url = reverse_lazy('datahub:incident_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'local_form' not in context:
            context['local_form'] = LocalForm()
        if 'arrestings_form' not in context:
            context['arrestings_form'] = ArrestingsForm()
        if 'guns_form' not in context:
            context['guns_form'] = GunsForm()
        if 'vehicles_form' not in context:
            context['vehicles_form'] = VehiclesForm()
        if 'money_form' not in context:
            context['money_form'] = MoneyForm()
        if 'drug_form' not in context:
            context['drug_form'] = DrugForm()
        if 'occurrencenature_form' not in context:
            context['occurrencenature_form'] = OcurrencenatureForm()

        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY

        return context

    def form_valid(self, form):
        self.object = form.save()

        # Processa o LocalForm
        local_form = LocalForm(self.request.POST)
        if local_form.is_valid():
            local_instance = local_form.save(commit=False)
            local_instance.incident = self.object
            local_instance.save()
        else:
            print(local_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form))

        # Processa o GunsForm
        guns_form = GunsForm(self.request.POST)
        if guns_form.is_valid():
            guns_instance = guns_form.save(commit=False)
            guns_instance.incident = self.object
            guns_instance.save()
        else:
            print(guns_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form))

        # Processa o VehiclesForm
        vehicles_form = VehiclesForm(self.request.POST)
        if vehicles_form.is_valid():
            vehicles_instance = vehicles_form.save(commit=False)
            vehicles_instance.incident = self.object
            vehicles_instance.save()
        else:
            print(vehicles_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form, vehicles_form=vehicles_form))

        # Processa o MoneyForm
        money_form = MoneyForm(self.request.POST)
        if money_form.is_valid():
            money_instance = money_form.save(commit=False)
            money_instance.incident = self.object
            money_instance.save()
        else:
            print(money_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form, vehicles_form=vehicles_form, money_form=money_form))

        # Processa o DrugForm
        drug_form = DrugForm(self.request.POST)
        if drug_form.is_valid():
            drug_instance = drug_form.save(commit=False)
            drug_instance.incident = self.object
            drug_instance.save()
        else:
            print(drug_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form, vehicles_form=vehicles_form, money_form=money_form, drug_form=drug_form))
        
        # Processa o OccurrenceNatureForm
        occurrencenature_form = OcurrencenatureForm(self.request.POST)
        if occurrencenature_form.is_valid():
            occurrencenature_instance = occurrencenature_form.save(commit=False)
            occurrencenature_instance.incident = self.object
            occurrencenature_instance.save()
            occurrencenature_form.save_m2m()  # Salva as relações ManyToMany
        else:
            print(occurrencenature_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form, vehicles_form=vehicles_form, money_form=money_form, drug_form=drug_form, occurrencenature_form=occurrencenature_form))
        return redirect(self.get_success_url())

class IncidentListView(ListView):
    model = Incident
    template_name = 'datahub/incident_list.html'  # Especifique o caminho para o seu template
    context_object_name = 'incidents' # O nome da variável para ser usada no template

class IncidentUpdateView(UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'datahub/incident_edit.html'
    success_url = reverse_lazy('datahub:incident_list')

    def get_object(self, queryset=None):
        CCD_key = self.kwargs.get('CCD_key')
        return get_object_or_404(Incident, CCD_key=CCD_key)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Incidente'

        # Obtendo instâncias relacionadas corretamente
        if 'local_form' not in context:
            context['local_form'] = LocalForm(instance=Local.objects.filter(incident=self.object).first())
        if 'guns_form' not in context:
            context['guns_form'] = GunsForm(instance=Guns.objects.filter(incident=self.object).first())
        if 'vehicles_form' not in context:
            context['vehicles_form'] = VehiclesForm(instance=Vehicles.objects.filter(incident=self.object).first())
        if 'money_form' not in context:
            context['money_form'] = MoneyForm(instance=Money.objects.filter(incident=self.object).first())
        if 'drug_form' not in context:
            context['drug_form'] = DrugForm(instance=Drug.objects.filter(incident=self.object).first())

        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY

        return context

    def form_valid(self, form):
        self.object = form.save()

        # Processa o LocalForm
        local_form = LocalForm(self.request.POST, instance=Local.objects.filter(incident=self.object).first())
        if local_form.is_valid():
            local_instance = local_form.save(commit=False)
            local_instance.incident = self.object
            local_instance.save()
        else:
            print(local_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form))

        # Processa o GunsForm
        guns_form = GunsForm(self.request.POST, instance=Guns.objects.filter(incident=self.object).first())
        if guns_form.is_valid():
            guns_instance = guns_form.save(commit=False)
            guns_instance.incident = self.object
            guns_instance.save()
        else:
            print(guns_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form))

        # Processa o VehiclesForm
        vehicles_form = VehiclesForm(self.request.POST, instance=Vehicles.objects.filter(incident=self.object).first())
        if vehicles_form.is_valid():
            vehicles_instance = vehicles_form.save(commit=False)
            vehicles_instance.incident = self.object
            vehicles_instance.save()
        else:
            print(vehicles_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form, vehicles_form=vehicles_form))

        # Processa o MoneyForm
        money_form = MoneyForm(self.request.POST, instance=Money.objects.filter(incident=self.object).first())
        if money_form.is_valid():
            money_instance = money_form.save(commit=False)
            money_instance.incident = self.object
            money_instance.save()
        else:
            print(money_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form, vehicles_form=vehicles_form, money_form=money_form))

        # Processa o DrugForm
        drug_form = DrugForm(self.request.POST, instance=Drug.objects.filter(incident=self.object).first())
        if drug_form.is_valid():
            drug_instance = drug_form.save(commit=False)
            drug_instance.incident = self.object
            drug_instance.save()
        else:
            print(drug_form.errors)
            return self.render_to_response(self.get_context_data(form=form, local_form=local_form, guns_form=guns_form, vehicles_form=vehicles_form, money_form=money_form, drug_form=drug_form))

        return redirect(self.get_success_url())

class IncidentDeleteView(DeleteView):
    model = Incident
    success_url = reverse_lazy('datahub:incident_list')  # Ajuste para o nome correto da sua URL de listagem

    def get_object(self, queryset=None):
        """Permite a busca de um incidente pelo seu CCD_key."""
        CCD_key = self.kwargs.get('CCD_key')
        return get_object_or_404(Incident, CCD_key=CCD_key)

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Ocorrência excluída com sucesso!')
        return super(IncidentDeleteView, self).post(request, *args, **kwargs)

class IncidentDetailView(DetailView):
    model = Incident
    template_name = 'datahub/incident_detail.html'
    context_object_name = 'incident'

    def get_object(self, queryset=None):
        CCD_key = self.kwargs.get('CCD_key')
        return get_object_or_404(Incident, CCD_key=CCD_key)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        incident = self.get_object()
        
        # Adicionar instâncias relacionadas ao contexto
        context['local'] = Local.objects.filter(incident=incident).first()
        context['guns'] = Guns.objects.filter(incident=incident).first()
        context['vehicles'] = Vehicles.objects.filter(incident=incident).first()
        context['drug'] = Drug.objects.filter(incident=incident).first()
        context['money'] = Money.objects.filter(incident=incident).first()
        context['occurrence_nature'] = OccurrenceNature.objects.filter(incident=incident).first()
        
        return context