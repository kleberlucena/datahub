
from django import forms
from apps.rpa_manager.models import Guarnicao
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


class GuarnicaoForm(forms.ModelForm):
    class Meta:
        model = Guarnicao
        fields = ['motorista', 
                  'piloto_remoto', 
                  'piloto_observador', 
                  'telefone', 
                  'local',
                  ]
        
        widgets = {
            'piloto_remoto': forms.HiddenInput(),    
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['motorista'].widget.attrs.update({
            'placeholder': 'Insira um motorista'
        })
        self.fields['piloto_observador'].widget.attrs.update({
            'placeholder': 'Insira um piloto observador'
        })
        self.fields['telefone'].widget.attrs.update({
            'placeholder': "Somente números, exemplo: '83988776655'"
        })
        self.fields['local'].widget.attrs.update({
            'placeholder': 'Insira o local de atuação'
        })

        campos = ['motorista', 
                  'piloto_remoto', 
                  'piloto_observador', 
                  'telefone', 
                  'local'
                  ]
        
        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')    

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if not telefone.isdigit():
            raise forms.ValidationError("Favor inserir dígitos numéricos. Por exemplo, '83988776655'.")
        return telefone
