from django import forms
from apps.rpa_manager.models import Incidentes
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


class IncidentesForm(forms.ModelForm):

    class Meta:
        model = Incidentes
        fields = ['operacao', 
                  'aeronave',
                  'local',
                  'ponto_de_referencia',
                  'relato', 
                  'data', 
                  ]
                
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = ['operacao', 
                  'aeronave',
                  'local',
                  'ponto_de_referencia',
                  'relato', 
                  'data',
                  ]

        
        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')


        self.fields['data'].widget.attrs.update({
            'class': 'form-control datetimepicker-input',
            'data-target': "#datetimepicker",
        })
        

