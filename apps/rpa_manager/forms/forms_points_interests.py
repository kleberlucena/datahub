from django import forms
from apps.rpa_manager.models import PontosDeInteresse, Relatorio
from apps.rpa_manager.utils.addAttributes import addAttributes

class PointsOfInterestForm(forms.ModelForm):
    class Meta:
        model = PontosDeInteresse
        fields = ['operacao', 
                  'is_temporary',
                  'date_initial',
                  'date_final',
                  'descricao', 
                  'latitude', 
                  'longitude']
        
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            }
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PointsOfInterestForm, self).__init__( *args, **kwargs)
        
        
        self.fields['descricao'].widget.attrs.update({
            'placeholder': 'Faça uma breve descrição do ponto de interesse.'
        })
        self.fields['date_initial'].widget.attrs.update({
            'placeholder': 'Insira a data inicial do evento.'
        })
        self.fields['date_final'].widget.attrs.update({
            'placeholder': 'Insira a data final do evento'
        })
        
        campos = ['operacao', 
                  'is_temporary',
                  'date_initial',
                  'date_final',
                  'descricao', 
                  'latitude', 
                  'longitude']
        
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')
            
            