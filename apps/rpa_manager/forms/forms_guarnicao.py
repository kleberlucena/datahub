
from django import forms
from apps.rpa_manager.models import Guarnicao

class GuarnicaoForm(forms.ModelForm):
    class Meta:
        model = Guarnicao
        fields = ['motorista', 'piloto_remoto', 'piloto_observador', 'telefone', 'local']
