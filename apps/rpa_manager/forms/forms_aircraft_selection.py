from django import forms
from apps.rpa_manager.models import Aeronave


class AeronaveSelectForm(forms.Form):
    aeronave = forms.ModelChoiceField(queryset=Aeronave.objects.all(), empty_label='Selecione uma aeronave')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['aeronave'].widget.attrs.update({'class': 'form-control aircraft_selection_form'})