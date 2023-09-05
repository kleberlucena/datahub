from django import forms
from apps.rpa_manager.models import Incidentes, Relatorio
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder

class IncidentesForm(forms.ModelForm):
    class Meta:
        model = Incidentes
        fields = ['operacao', 
                  'aeronave',
                  'piloto',
                  'local',
                  'ponto_de_referencia',
                  'relato', 
                  'data', 
                  ]
                
        widgets = {
            'piloto': forms.HiddenInput(),
        }
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user:
            if user.is_superuser:
                self.fields['operacao'].queryset = Relatorio.objects.all()
            else:
                self.fields['operacao'].queryset = Relatorio.objects.filter(militar=user)
              
        addPlaceholder(self, 'ponto_de_referencia', 'Insira um ponto de referência do local do incidente.' )              
        addPlaceholder(self, 'relato', 'Elabore um relato com os fatos ocorridos no incidente.' )              
              
                
        campos = ['operacao', 
                  'aeronave',
                  'local',
                  'ponto_de_referencia',
                  'relato', 
                  'data',
                  ]

        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')


        self.fields['data'].widget.attrs.update({
            'class': 'form-control datetimepicker-input',
            'data-target': "#datetimepicker",
        })
        