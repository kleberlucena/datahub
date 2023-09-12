from django import forms
from apps.rpa_manager.models import RiskAssessment, Assessment
from apps.rpa_manager.utils.addAttributes import addAttributes
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder


class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['operational_scenario', 'operator', 'date', 'expiration_date', 'cnpj', 'aircrafts', 'apllied_legislation', 'keep_distance_from_3rd', 'pilots_capabilities', 'accident_procedure', 'info_responsible']
        
        widgets = {
            'info_responsible': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'operational_scenario', 'Insira o cenário operacional')
        addPlaceholder(self, 'operator', 'Insira o operador responsável')
        addPlaceholder(self, 'cnpj', 'Insira o cnpj do operador')
        addPlaceholder(self, 'apllied_legislation', 'Insira as legislações aplicáveis')
        addPlaceholder(self, 'accident_procedure', 'Insira os procedimentos em caso de acidentes')
        
        self.fields['date'].widget.attrs.update({
            'required': True
        })
        self.fields['expiration_date'].widget.attrs.update({
            'required': True
        })
        self.fields['aircrafts'].widget.attrs.update({
            'required': True
        })
        
        campos = ['operational_scenario' ,'operator', 'date', 'expiration_date', 'cnpj', 'aircrafts', 'apllied_legislation', 'accident_procedure']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')
            
class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['situation', 'probability_of_occurrence', 'severity_of_occurrence', 'hierarchy_authorization', 'mitigation_measures_risk']
        exclude = ['risk', 'tolerability']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        addPlaceholder(self, 'hierarchy_authorization', 'Insira o grau hierárquico de quem autorizou' )
        addPlaceholder(self, 'mitigation_measures_risk', 'Informe como será feita a mitigação dos riscos' )

        campos = ['situation', 'probability_of_occurrence', 'severity_of_occurrence', 'hierarchy_authorization', 'mitigation_measures_risk']
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')