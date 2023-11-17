from django import forms
from apps.rpa_manager.models import *
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder


class IncidentsForm(forms.ModelForm):
    class Meta:
        model = Incidents
        fields = ['operation', 
                  'aircraft',
                  'remote_pilot',
                  'location',
                  'reference_point',
                  'report', 
                  'police_incident_number',
                  'date', 
                  ]
                
        widgets = {
            'remote_pilot': forms.HiddenInput(),
        }
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user:
            if user.is_superuser:
                self.fields['operation'].queryset = Report.objects.all()
            else:
                self.fields['operation'].queryset = Report.objects.filter(remote_pilot=user)
              
        addPlaceholder(self, 'reference_point', 'Insira um ponto de referência do local do incidente.' )              
        addPlaceholder(self, 'report', 'Elabore um relato com os fatos ocorridos no incidente.' )              
              
                
        campos = ['operation', 
                  'aircraft',
                  'location',
                  'reference_point',
                  'report', 
                  'police_incident_number',
                  'date', 
                  ]

        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')


        self.fields['date'].widget.attrs.update({
            'class': 'form-control datetimepicker-input',
            'data-target': "#datetimepicker",
        })
        