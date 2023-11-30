from django import forms
from apps.rpa.models import Aircraft


class AircraftSelectionForm(forms.Form):
    aircraft = forms.ModelChoiceField(queryset=Aircraft.objects.all(), empty_label='Selecione uma aeronave')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['aircraft'].widget.attrs.update({'class': 'form-control aircraft_selection_form'})