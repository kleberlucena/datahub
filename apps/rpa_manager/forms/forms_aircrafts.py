from django import forms
from apps.rpa_manager.models import Aircraft
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder


class AircraftsForm(forms.ModelForm):

    class Meta:
        model = Aircraft
        fields = ['prefix', 
                  'model',
                  'brand',
                  'aircraft_image',
                  'location',
                  'in_use']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        addPlaceholder(self, 'prefix', 'Insira o prefixo da aeronave' )
        addPlaceholder(self, 'model', 'Insira o modelo da aeronave' )
        addPlaceholder(self, 'brand', 'Insira a marca da aeronave' )

        campos = ['prefix', 'model', 'brand','aircraft_image' , 'location', 'in_use']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')