
from django import forms
from apps.rpa_manager.models import PoliceGroup
from apps.rpa_manager.utils.addAttributes import addAttributes


class PoliceGroupForm(forms.ModelForm):
    class Meta:
        model = PoliceGroup
        fields = ['driver', 
                  'remote_pilot', 
                  'observer_pilot', 
                  'phone', 
                  'location',
                  ]
        
        widgets = {
            'remote_pilot': forms.HiddenInput(),    
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['driver'].widget.attrs.update({
            'placeholder': 'Insira um motorista'
        })
        self.fields['observer_pilot'].widget.attrs.update({
            'placeholder': 'Insira um piloto observador'
        })
        self.fields['phone'].widget.attrs.update({
            'placeholder': "Somente números, exemplo: '83988776655'"
        })
        self.fields['location'].widget.attrs.update({
            'placeholder': 'Insira o local de atuação'
        })

        campos = ['driver', 
                  'remote_pilot', 
                  'observer_pilot', 
                  'phone', 
                  'location',
                  ]
        
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')    
            
    def clean_telefone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Favor inserir dígitos numéricos. Por exemplo, '83988776655'.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        remote_pilot = cleaned_data.get('remote_pilot')
        observer_pilot = cleaned_data.get('observer_pilot')
        
        if remote_pilot == observer_pilot:
            self.add_error('remote_pilot', "O piloto remoto não pode ser o mesmo que o piloto observador.")
            self.add_error('observer_pilot', "O piloto observador não pode ser o mesmo que o piloto remoto.")
            
            