from django import forms
from apps.rpa.models import Legislation
from apps.rpa.utils.addAttributes import addAttributes
from apps.rpa.utils.addPlaceholderToField import addPlaceholder

class LegislationForm(forms.ModelForm):
    
    class Meta:
        model = Legislation
        fields = ['title', 'description',  'in_effect', 'date_published', 'legislation_file']
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'date_published': 'Data de publicação',
            'in_effect': 'Está em vigor'
        }
        widgets = {
            'date_published': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'title', 'Insira o título da legislação')
        addPlaceholder(self, 'description', 'Insira uma descrição sobre o que a legislação trata.')
        
        campos = ['title', 'description' , 'date_published']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')