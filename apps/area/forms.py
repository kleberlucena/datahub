from django import forms
from . import models


class AreaForm(forms.ModelForm):
    class Meta:
        model = models.Area
        fields = ['name','description']
        labels = {
            'name': 'Nome da area',
            'description': 'Informações adicionais',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. 1BPM ou QPP1 ou CPRM'}), #ESTÁ DE MANEIRA GENÉRICA
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se houver, insira informações adicionais'}),
        }