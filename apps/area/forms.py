from django import forms
from . import models


class AreaForm(forms.ModelForm):
    class Meta:
        model = models.Area
        fields = ['name','description','area_polygon', 'category']
        labels = {
            'name': 'Nome da area',
            'description': 'Descrição',
            'area_polygon' : 'Área delimitada',
            'category' : 'Categoria'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. 1BPM ou QPP1 ou CPRM'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. Área do 1BPM'}),
            'area_polygon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name','description']
        labels = {
            'name': 'Nome da categoria',
            'description': 'Descrição',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. Batalhão, Comunidade ou Evento'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. Batalhão de Polícia Militar ou Bloco Carnavalesco ou Escola de Ensino Fundamental'}),
        }