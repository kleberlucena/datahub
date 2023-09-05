from django import forms
from apps.rpa_manager.models import TypeOfBattery
from apps.rpa_manager.utils.addAttributes import addAttributes

class TypeOfBatteryForm(forms.ModelForm):
    class Meta:
        model = TypeOfBattery
        fields = ['name', 'recommended_cicles', 'alert_cicles', 'critical_cicles']
        
        labels = {
            'name': 'Nome',
            'recommended_cicles': 'Ciclos recomendado',
            'alert_cicles': 'Ciclos alerta',
            'critical_cicles': 'Ciclos crítico'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Insira um nome referente ao modelo, ex: Bateria Phantom'    
        })
        
        campos = ['name', 'recommended_cicles', 'alert_cicles', 'critical_cicles']

        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')