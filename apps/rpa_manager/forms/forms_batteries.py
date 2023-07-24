from django import forms
from apps.rpa_manager.models import Bateria
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


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

        campos = ['numeracao', 'num_ciclos', 'ciclos_maximo', 'aeronave']

        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')