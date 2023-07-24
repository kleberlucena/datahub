from django import forms
from apps.rpa_manager.models import Aeronave
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


class AeronavesForm(forms.ModelForm):

    class Meta:
        model = Aeronave
        fields = ['prefixo', 'modelo',
                  'marca', 'local',
                  'em_uso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        campos = ['prefixo', 'modelo', 'marca', 'local', 'em_uso']

        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')