from django import forms
from django.core.exceptions import ValidationError
from apps.rpa_manager.models import *
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['title', 
                  'observer_pilot', 
                  'who_requested', 
                  'who_authorized', 
                  'location', 
                  'latitude', 
                  'longitude', 
                  'aircraft', 
                  'user'
                  ]
        
        widgets = {
                   'user': forms.HiddenInput(),
                   'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'completed': forms.HiddenInput(),
                   }

    def clean_aircraft(self):
        aircraft = self.cleaned_data['aircraft']
        if aircraft.in_use:
            raise forms.ValidationError('A aeronave está em uso e não pode ser selecionada.')
        return aircraft
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        addPlaceholder(self, 'title', 'Informe um título para operação')
        addPlaceholder(self, 'who_authorized', 'Informe quem autorizou a operação')
        addPlaceholder(self, 'who_requested', 'Informe um título para operação')
        
        self.fields['aircraft'].widget.attrs.update({
            'class': 'aircraft_escolha'
        })
        self.fields['latitude'].widget.attrs.update({
            'required': True
        })
        self.fields['longitude'].widget.attrs.update({
            'required': True
        })

        self.fields['aircraft'].queryset = Aircraft.objects.filter(in_use=False)
        
        campos = ['title', 
                  'observer_pilot', 
                  'who_requested',
                  'who_authorized', 
                  'location', 
                  'latitude',
                  'longitude',
                  'aircraft', 
                  'user']
        
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')
            
    def clean(self):
        cleaned_data = super().clean()
        remote_pilot = cleaned_data.get('user')
        observer_pilot = cleaned_data.get('observer_pilot')
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        
        if remote_pilot == observer_pilot:
            self.add_error('user', "O piloto remoto não pode ser o mesmo que o piloto observador.")
            self.add_error('piloto_observador', "O piloto observador não pode ser o mesmo que o piloto remoto.")
        if latitude == 0.0:
            self.add_error('latitude', "Latitude ou Longitude inválidos (marque um ponto no mapa)")
        if longitude == 0.0:
            self.add_error('longitude', "Latitude ou Longitude inválidos (marque um ponto no mapa)")
        
        return cleaned_data
