from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.models import inlineformset_factory
from apps.georeference.models import Area, Category
from django import forms
from django.forms.models import inlineformset_factory
from .models import Incident, Local, Guns, Vehicles, Drug, Money, DriRegion, NiIndication, SupportingNI, OccurrenceNature

class IncidentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Salvar'))

    class Meta:
        model = Incident
        fields = ['email_address', 'occurrence_date', 'dri_region', 'ni_area', 'ni_indication', 'ostensive_arresting', 'supporting_ni', 'occurrence_nature']
        labels = {
            'email_address': 'Endereço de E-mail',
            'occurrence_date': 'Data da Ocorrência',
            'dri_region': 'Região DRI',
            'ni_area': 'NI Área',
            'ni_indication': 'Ni responsável pela indicação',
            'ostensive_arresting': 'Ostensivo responsável pela prisão',
            'supporting_ni': 'NI que prestou apoio',
            'occurrence_nature': 'Natureza da ocorrência',
        }
        widgets = {
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'occurrence_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dri_region': forms.Select(attrs={'class': 'form-control'}),
            'ni_area': forms.Select(attrs={'class': 'form-control'}),
            'ni_indication': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'ostensive_arresting': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'supporting_ni': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'occurrence_nature': forms.Select(attrs={'class': 'form-control'}),
        }
          
class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['endereco','latitude','longitude']  
        labels = {
            'endereco': 'Endereço',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }
        widgets = {
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class GunsForm(forms.ModelForm):
    class Meta:
        model = Guns
        fields = ['guns_revolver', 'guns_pistol', 'guns_bpistol', 'guns_shotgun', 'guns_carbine', 'guns_mg', 'guns_rifle', 'guns_explosive', 'guns_clump', 'guns_handcrafted', 'guns_simulacrum', 'guns_ammunition', 'guns_bodyarmor']  
        labels = {
            'guns_revolver': 'Revólver',
            'guns_pistol': 'Pistola',
            'guns_bpistol': 'Pistolão',
            'guns_shotgun': 'Espingarda',
            'guns_carbine': 'Carabina',
            'guns_mg': 'Metralhadora',
            'guns_rifle': 'Rifle',
            'guns_explosive': 'Explosivo',
            'guns_clump': 'Cassetete',
            'guns_handcrafted': 'Arma Artesanal',
            'guns_simulacrum': 'Simulacro',
            'guns_ammunition': 'Munição',
            'guns_bodyarmor': 'Colete Balístico',
        }
        widgets = {
            'guns_revolver': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_pistol': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_bpistol': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_shotgun': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_carbine': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_mg': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_rifle': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_explosive': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_clump': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_handcrafted': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_simulacrum': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_ammunition': forms.NumberInput(attrs={'class': 'form-control'}),
            'guns_bodyarmor': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VehiclesForm(forms.ModelForm):
    class Meta:
        model = Vehicles
        fields = ['recovered_car', 'recovered_moto', 'recovered_pickup', 'recovered_truck', 'recovered_other', 'administratively_seized_car', 'administratively_seized_moto', 'administratively_seized_pickup', 'administratively_seized_truck', 'administratively_seized_other']
        labels = {
            'recovered_car': 'Carro Recuperado',
            'recovered_moto': 'Moto Recuperada',
            'recovered_pickup': 'Pick-Up Recuperada',
            'recovered_truck': 'Caminhão Recuperado',
            'recovered_other': 'Outros Veículos Recuperados',
            'administratively_seized_car': 'Carro Apreendido Administrativamente',
            'administratively_seized_moto': 'Moto Apreendida Administrativamente',
            'administratively_seized_pickup': 'Pick-Up Apreendida Administrativamente',
            'administratively_seized_truck': 'Caminhão Apreendido Administrativamente',
            'administratively_seized_other': 'Outros Apreendidos Administrativamente',
        }
        widgets = {
            'recovered_car': forms.NumberInput(attrs={'class': 'form-control'}),
            'recovered_moto': forms.NumberInput(attrs={'class': 'form-control'}),
            'recovered_pickup': forms.NumberInput(attrs={'class': 'form-control'}),
            'recovered_truck': forms.NumberInput(attrs={'class': 'form-control'}),
            'recovered_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'administratively_seized_car': forms.NumberInput(attrs={'class': 'form-control'}),
            'administratively_seized_moto': forms.NumberInput(attrs={'class': 'form-control'}),
            'administratively_seized_pickup': forms.NumberInput(attrs={'class': 'form-control'}),
            'administratively_seized_truck': forms.NumberInput(attrs={'class': 'form-control'}),
            'administratively_seized_other': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['artane', 'lsd', 'ecstasy', 'lolo', 'crack', 'haxixe', 'tch', 'marihuana', 'skank', 'cocaine']
        labels = {
            'artane': 'Artane',
            'lsd': 'LSD',
            'ecstasy': 'Ecstasy',
            'lolo': 'Loló',
            'crack': 'Crack',
            'haxixe': 'Haxixe',
            'tch': 'THC',
            'marihuana': 'Maconha',
            'skank': 'Skank',
            'cocaine': 'Cocaína',
        }
        widgets = {
            'artane': forms.NumberInput(attrs={'class': 'form-control'}),
            'lsd': forms.NumberInput(attrs={'class': 'form-control'}),
            'ecstasy': forms.NumberInput(attrs={'class': 'form-control'}),
            'lolo': forms.NumberInput(attrs={'class': 'form-control'}),
            'crack': forms.NumberInput(attrs={'class': 'form-control'}),
            'haxixe': forms.NumberInput(attrs={'class': 'form-control'}),
            'tch': forms.NumberInput(attrs={'class': 'form-control'}),
            'marihuana': forms.NumberInput(attrs={'class': 'form-control'}),
            'skank': forms.NumberInput(attrs={'class': 'form-control'}),
            'cocaine': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MoneyForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['amount']
        labels = {
            'amount': 'Valor em Dinheiro',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

LocalFormSet = inlineformset_factory(Incident, Local, form=LocalForm, can_delete=False, extra=1)
GunsFormSet = inlineformset_factory(Incident, Guns, form=GunsForm, can_delete=False, extra=1)
VehiclesFormSet = inlineformset_factory(Incident, Vehicles, form=VehiclesForm, can_delete=False, extra=1)
DrugFormSet = inlineformset_factory(Incident, Drug, form=DrugForm, can_delete=False, extra=1)
MoneyFormSet = inlineformset_factory(Incident, Money, form=MoneyForm, can_delete=False, extra=1)


