from django import forms

from apps.rpa.models import PoliceGroup

class PoliceGroupForm2(forms.ModelForm):
 
    class Meta:
        model = PoliceGroup
        fields = ['driver', 
                  'remote_pilot', 
                  'observer_pilot', 
                  'phone', 
                  'location',]
        
        widgets = {
            'remote_pilot': forms.HiddenInput(),    
        }
        
    def __init__(self, *args, **kwargs):
        print('No form__init__')
        super().__init__(*args, **kwargs)