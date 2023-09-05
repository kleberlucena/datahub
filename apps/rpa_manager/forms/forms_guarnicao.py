
from django import forms
from apps.rpa_manager.models import Guarnicao
from apps.rpa_manager.utils.addAttributes import addAttributes


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
            addAttributes(self, campo, campo, 'form-control')    
            
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if not telefone.isdigit():
            raise forms.ValidationError("Favor inserir dígitos numéricos. Por exemplo, '83988776655'.")
        return telefone

    def clean(self):
        cleaned_data = super().clean()
        piloto_remoto = cleaned_data.get('piloto_remoto')
        piloto_observador = cleaned_data.get('piloto_observador')
        
        if piloto_remoto == piloto_observador:
            self.add_error('piloto_remoto', "O piloto remoto não pode ser o mesmo que o piloto observador.")
            self.add_error('piloto_observador', "O piloto observador não pode ser o mesmo que o piloto remoto.")
            
            