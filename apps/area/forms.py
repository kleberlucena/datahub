from django import forms
from . import models


class AreaForm(forms.ModelForm):
    class Meta:
        model = models.Area
        fields = ['name','details']
        labels = {
            'name': 'Nome da area',
            'details': 'Informações adicionais',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. 1BPM ou QPP1 ou CPRM'}), #ESTÁ DE MANEIRA GENÉRICA
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se houver, insira informações adicionais'}),
        }