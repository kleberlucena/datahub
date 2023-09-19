from django import forms
from apps.rpa_manager.models import Battery
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder

class BateriaForm(forms.ModelForm):
    
    class Meta:
        model = Battery
        exclude = ['maleta']

        labels = {
            'number': 'Numeração',
            'num_cicles': 'Número de ciclos',
            'maximum_cicles': 'Número máximo de ciclos',
            'aircraft': 'Está em uso na aeronave'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'number', 'Insira a numeração da bateria')
        addPlaceholder(self, 'num_cicles', 'Insira o número de ciclos atual bateria')
        
        campos = ['number', 'num_cicles', 'maximum_cicles', 'aircraft']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')