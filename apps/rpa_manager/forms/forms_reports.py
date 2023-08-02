from django import forms
from apps.rpa_manager.models import Relatorio
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control


class RelatorioFormulario(forms.ModelForm):
    status_missao = forms.BooleanField(
        label="Concluir missão?",
    )

    class Meta:
        model = Relatorio
        fields = [
            'titulo', 'militar',
            'piloto_observador', 'quem_solicitou', 
            'quem_autorizou','data',
            'data_final',
            'horario_inicial', 'horario_final',
            'local', 'latitude', 'longitude', 'arquivo_solicitacao',
            'num_sarpas', 'entidade_apoiada',
            'natureza_de_voo',
            'tipo_de_operacao', 'aeronave',
            'numero_ficha_oc',  
            'relato_da_missao',
        ]
        exclude = ['missao']
        
        labels = {
            'militar': '',
            'horario_inicial': 'Horário inicial',
            'horario_final': 'Horário final',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'arquivo_solicitacao': 'Arquivo de solicitação',
            'entidade apoiada': 'Entidade apoiada',
            'num_sarpas': 'Número SARPAS/Protocolo',
            'natureza_de_voo': 'Natureza do voo',
            'tipo_de_operacao': 'Tipo de operação',
            'relato_da_missao': 'Relato da missão',
            'data': 'Data inicial',
            'data_final': 'Data final',
            'numero_ficha_oc': 'Número ficha ocorrência CIOP'
        }
        
        widgets = {
            'militar': forms.HiddenInput(),
            'horario_inicial': forms.TimeInput(attrs={'type': 'time'}),
            'horario_final': forms.TimeInput(attrs={'type': 'time'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'data_final': forms.DateInput(attrs={'type': 'date'}),
            'num_sarpas': forms.Textarea(attrs={
                'placeholder': 'Informe o Protocolo ou nº SARPAS',
                'rows': 1}),
            'relato_da_missao': forms.Textarea(attrs={'placeholder': 'Descreva a alteração'})
        }
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = [
            'titulo', 
            'piloto_observador',
            'quem_solicitou',
            'quem_autorizou', 
            'data',
            'data_final', 
            'horario_inicial', 
            'horario_final', 
            'local',
            'latitude',
            'longitude', 
            'num_sarpas',
            'entidade_apoiada', 
            'natureza_de_voo', 
            'tipo_de_operacao', 
            'aeronave', 
            'numero_ficha_oc',
            'relato_da_missao'
        ]
        
        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')
            
        self.fields['titulo'].widget.attrs['readonly'] = True
        
        self.fields['status_missao'].widget.attrs.update({
            'class': 'form-check form-switch', 
        })

        self.fields['arquivo_solicitacao'].widget.attrs.update({
            'class': 'p-3',
            'accept': "application/pdf", 
        })