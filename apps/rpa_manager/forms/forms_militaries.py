from django import forms
from apps.rpa_manager.models import Militar
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


class MilitarForm(forms.ModelForm):
    
    class Meta:
        model = Militar
        fields = ['nome_de_guerra', 'total_de_horas_voo', 'matricula', 'roles']
    
    def clean_matricula(self):
        valor = self.cleaned_data['matricula']
        if self.instance.pk is None and Militar.objects.filter(matricula=valor).exists():
            raise forms.ValidationError('Este valor já existe. Por favor, escolha outro.')
        return valor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['roles'].widget.attrs.update({'data-placeholder': 'Selecione as funções'})

        campos = ['nome_de_guerra', 'total_de_horas_voo', 'matricula', 'roles']
        
        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')