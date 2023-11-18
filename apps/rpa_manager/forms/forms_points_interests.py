from django import forms
from apps.rpa_manager.models import PointsOfInterest
from apps.rpa_manager.utils.addAttributes import addAttributes


class PointsOfInterestForm(forms.ModelForm):
    class Meta:
        model = PointsOfInterest
        fields = ['operation', 
                  'is_temporary',
                  'initial_date',
                  'final_date',
                  'description', 
                  'latitude', 
                  'longitude']
        
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            }
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PointsOfInterestForm, self).__init__( *args, **kwargs)
                
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Faça uma breve descrição do ponto de interesse.'
        })
        self.fields['initial_date'].widget.attrs.update({
            'placeholder': 'Insira a data inicial do evento.'
        })
        self.fields['final_date'].widget.attrs.update({
            'placeholder': 'Insira a data final do evento'
        })
        
        campos = ['operation', 
                  'is_temporary',
                  'initial_date',
                  'final_date',
                  'description', 
                  'latitude', 
                  'longitude']
        
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')
            
            