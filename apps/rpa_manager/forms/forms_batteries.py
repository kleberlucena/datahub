from django import forms
from apps.rpa_manager.models import Bateria
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder

class BateriaForm(forms.ModelForm):
    
    class Meta:
        model = Bateria
        exclude = ['maleta']

        labels = {
            'numeracao': 'Numeração',
            'num_ciclos': 'Número de ciclos',
            'ciclos_maximo': 'Número máximo de ciclos',
            'aeronave': 'Está em uso na aeronave'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'numeracao', 'Insira a numeração da bateria')
        addPlaceholder(self, 'num_ciclos', 'Insira o número de ciclos atual bateria')
        
        campos = ['numeracao', 'num_ciclos', 'ciclos_maximo', 'aeronave']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')