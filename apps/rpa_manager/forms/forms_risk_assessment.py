from django import forms
from apps.rpa_manager.models import RiskAssessment, Assessment
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder


class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['operator', 'date', 'cpf', 'aircrafts', 'apllied_legislation', 'keep_distance_from_3rd', 'pilots_capabilities', 'accident_procedure']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'operator', 'Insira o operador responsável' )
        addPlaceholder(self, 'cpf', 'Insira o cpf do operador' )
        addPlaceholder(self, 'apllied_legislation', 'Insira as legislações aplicáveis')
        addPlaceholder(self, 'accident_procedure', 'Insira os procedimentos em caso de acidentes')

        campos = ['operator', 'date', 'cpf', 'aircrafts', 'apllied_legislation', 'accident_procedure']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')
            
class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['situation', 'probability_of_occurrence', 'risk', 'severity_of_occurrence', 'hierarchy_authorization', 'tolerability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'hierarchy_authorization', 'Insira o grau hierárquico de quem autorizou' )

        campos = ['situation', 'probability_of_occurrence', 'risk', 'severity_of_occurrence', 'hierarchy_authorization', 'tolerability']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')