from django import forms
from apps.rpa_manager.models import Missao, Aeronave
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


class MissaoFormulario(forms.ModelForm):
    
    class Meta:
        model = Missao
        fields = ['titulo', 
                  'piloto_observador', 
                  'quem_solicitou', 
                  'quem_autorizou', 
                  'local', 
                  'aeronave', 
                  'usuario'
                  ]
        
        labels = {
            'usuario': '',
        }
        
        widgets = {'usuario': forms.HiddenInput(),
                   'titulo': forms.TextInput(attrs={'class': 'form-control'}),
                   'concluida': forms.HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['aeronave'].queryset = Aeronave.objects.filter(em_uso=False)
        self.fields['titulo'].widget.attrs.update({
            'placeholder': 'Informe um título para operação'
        })
        self.fields['quem_autorizou'].widget.attrs.update({
            'placeholder': 'Informe quem autorizou a operação'
        })
        self.fields['quem_solicitou'].widget.attrs.update({
            'placeholder': 'Informe quem solicitou a operação'
        })
        self.fields['aeronave'].widget.attrs.update({
            'class': 'aeronave_escolha'
        })
        
        campos = ['titulo', 
                  'piloto_observador', 
                  'quem_solicitou',
                  'quem_autorizou', 
                  'local', 
                  'aeronave', 
                  'usuario']
        
        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')