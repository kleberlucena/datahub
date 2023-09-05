from django import forms
from apps.rpa_manager.models import Aeronave
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder


class AeronavesForm(forms.ModelForm):

    class Meta:
        model = Aeronave
        fields = ['prefixo', 
                  'modelo',
                  'marca',
                  'imagem_aeronave',
                  'local',
                  'em_uso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'prefixo', 'Insira o prefixo da aeronave' )
        addPlaceholder(self, 'modelo', 'Insira o modelo da aeronave' )
        addPlaceholder(self, 'marca', 'Insira a marca da aeronave' )

        campos = ['prefixo', 'modelo', 'marca','imagem_aeronave' , 'local', 'em_uso']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')