from django import forms
from apps.rpa_manager.models import PontosDeInteresse
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


class PointsOfInterestForm(forms.ModelForm):
    class Meta:
        model = PontosDeInteresse
        fields = ['operacao', 
                  'descricao', 
                  'latitude', 
                  'longitude']
        
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['descricao'].widget.attrs.update({
            'placeholder': 'Faça uma breve descrição do ponto de interesse.'
        })
        
        campos = ['operacao', 
                  'descricao', 
                  'latitude', 
                  'longitude']
        
        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')