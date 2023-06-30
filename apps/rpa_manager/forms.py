from django import forms

from .models import *


def adiciona_atributo_classe_ao_widget(aponta_para_o_objecto_da_classe, campo, novo_attrs1, novo_attrs2):
    aponta_para_o_objecto_da_classe.fields[campo].widget.attrs.update({
        'class': str(novo_attrs1) + '_escolha ' +  str(novo_attrs2)
    })


camposCheckboxesChecklist = [
        'baterias_carregadas',
        'bateria_controle_carregada',
        'corpo',
        'hastes_motor',
        'helices',
        'gimbal',
        'holofote',
        'auto_falante',
        'luz_estroboscopica',
        'cabos',
        'carregador',
        'fonte',
        'smart_controller',
        'controle',
        'cartao_sd',
        'IMU',
        'compass',
        'sinal_transmissao',
        'sistema_rtk_ppk',
        'sinal_de_video',
        'telemetria',
        'paraquedas',
    ]
    
class MissaoFormulario(forms.ModelForm):
    
    class Meta:
        model = Missao
        fields = ['titulo', 'piloto_observador', 'local', 'aeronave', 'usuario']
        
        labels = {
            'usuario': '',
        }
        
        widgets = {'usuario': forms.HiddenInput(),
                   'concluida': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = ['titulo', 'piloto_observador', 'local', 'aeronave', 'usuario']
        
        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')
        
             
class RelatorioFormulario(forms.ModelForm):
    status_missao = forms.BooleanField(
        label="Concluir missão?",
    )
     
    class Meta:
        model = Relatorio
        # fields = '__all__'
        exclude = ['missao']
        
        labels = {
            'militar': '',
            'horario_inicial': 'Horário inicial',
            'horario_final': 'Horário final',
            'arquivo_solicitacao': 'Arquivo de solicitação',
            'num_sarpas': 'Número SARPAS/Protocolo',
            'opm_apoiada': 'OPM que foi apoiada',
            'unidade_apoiada': 'Unidade que foi apoiada',
            'natureza_de_voo': 'Natureza do voo',
            'tipo_de_operacao': 'Tipo de operação',
            'relato_da_missao': 'Relato da missão'
        }
        
        widgets = {
            'militar': forms.HiddenInput(),
            'horario_inicial': forms.TimeInput(attrs={'type': 'time'}),
            'horario_final': forms.TimeInput(attrs={'type': 'time'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'num_sarpas': forms.Textarea(attrs={'placeholder': 'Informe o Protocolo ou nº SARPAS'}),
            'relato_da_missao': forms.Textarea(attrs={'placeholder': 'Descreva a alteração'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = [
            'titulo', 
            'piloto_observador', 
            'data', 
            'horario_inicial', 
            'horario_final', 
            'local', 
            'num_sarpas', 
            'opm_apoiada', 
            'unidade_apoiada', 
            'natureza_de_voo', 
            'tipo_de_operacao', 
            'aeronave', 
            'relato_da_missao'
        ]
        
        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')
            
        self.fields['titulo'].widget.attrs['readonly'] = True
        
        self.fields['status_missao'].widget.attrs.update({
            'class': 'form-check form-switch', 
        })
        

                
class MilitarForm(forms.ModelForm):
    
    class Meta:
        model = Militar
        # fields = '__all__'
        exclude = ['esta_em_missao']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = ['usuario', 'nome_de_guerra', 'total_de_horas_voo', 'matricula']
        
        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')

class AeronavesForm(forms.ModelForm):

    class Meta:
        model = Aeronave
        # fields = '__all__'
        exclude = ['maleta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        campos = ['prefixo', 'modelo', 'marca', 'local']

        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')
        
class BateriaForm(forms.ModelForm):
    
    class Meta:
        model = Bateria
        exclude = ['maleta']

        labels = {
            'numeracao': 'Numeração',
            'num_ciclos': 'Número de ciclos',
            'ciclos_maximo': 'Número máximo de ciclos',
            'aeronave': 'Está em uso na aeronave'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        campos = ['numeracao', 'num_ciclos', 'ciclos_maximo', 'aeronave']

        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')
        
class ChecklistForm(forms.ModelForm):
    
    class Meta:
        model = Checklist
        fields = '__all__'

        labels = {
            'piloto': '',
            'num_baterias': 'Número de baterias',
            'num_helices': 'Número de hélices',
        }
        widgets = {'piloto': forms.HiddenInput()}
        
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = ['aeronave', 'num_baterias', 'num_helices', 'alteracoes']
        
        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')
        
        for campo in camposCheckboxesChecklist:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'checklist_item')


        