from django import forms
from apps.rpa_manager.models import Report
from apps.rpa_manager.utils.addAttributes import addAttributes


class ReportForm(forms.ModelForm):
    completed = forms.BooleanField(
        label="Concluir missão?",
    )

    class Meta:
        model = Report
        fields = [
            'title', 'remote_pilot',
            'observer_pilot', 'who_requested', 
            'who_authorized','date',
            'final_date',
            'initial_time', 'final_time',
            'location', 'latitude', 'longitude', 'decea_request_file',
            'num_sarpas', 'entity_support',
            'flight_nature',
            'type_of_operation', 'aircraft',
            'police_incident_number',  
            'operation_report',
        ]
        
        labels = {
            'remote_pilot': '',
            'initial_time': 'Horário inicial',
            'final_time': 'Horário final',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'decea_request_file': 'Arquivo de solicitação',
            'entity_support': 'Entidade apoiada',
            'num_sarpas': 'Número SARPAS/Protocolo',
            'flight_nature': 'Natureza do voo',
            'type_of_operation': 'Tipo de operação',
            'operation_report': 'Relato da missão',
            'date': 'Data inicial',
            'final_date': 'Data final',
            'police_incident_number': 'Número ficha ocorrência CIOP'
        }
        
        widgets = {
            'remote_pilot': forms.HiddenInput(),
            'initial_time': forms.TimeInput(attrs={'type': 'time'}),
            'final_time': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'final_date': forms.DateInput(attrs={'type': 'date'}),
            'num_sarpas': forms.Textarea(attrs={
                'placeholder': 'Informe o Protocolo ou nº SARPAS',
                'rows': 1}),
            'operation_report': forms.Textarea(attrs={'placeholder': 'Descreva a alteração'})
        }
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = [
            'title', 
            'remote_pilot',
            'observer_pilot',
            'who_requested',
            'who_authorized', 
            'date',
            'final_date', 
            'initial_time', 
            'final_time', 
            'location',
            'latitude',
            'longitude', 
            'num_sarpas',
            'entity_support', 
            'flight_nature', 
            'type_of_operation', 
            'aircraft', 
            'police_incident_number',
            'operation_report'
        ]
        
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')
            
        self.fields['final_time'].required = False 
        
        self.fields['title'].widget.attrs['readonly'] = True
        
        self.fields['completed'].widget.attrs.update({
            'class': 'form-check form-switch', 
        })

        self.fields['decea_request_file'].widget.attrs.update({
            'class': 'p-3',
            'accept': "application/pdf", 
        })
        
        
    def clean(self):
        cleaned_data = super().clean()
        remote_pilot = cleaned_data.get('remote_pilot')
        observer_pilot = cleaned_data.get('observer_pilot')
        
        if remote_pilot == observer_pilot:
            self.add_error('remote_pilot', "O piloto remoto não pode ser o mesmo que o piloto observador.")
            self.add_error('observer_pilot', "O piloto observador não pode ser o mesmo que o piloto remoto.")
            