from django import forms
from .models import *

def adiciona_atributo_classe_ao_widget(this_obj, campo, attrs1 = '', attrs2 = '', attrs3 = ''):
    this_obj.fields[campo].widget.attrs.update({
        'class': str(attrs1) + '_escolha ' +  str(attrs2) + str(attrs3)
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
        fields = ['titulo', 
                  'piloto_observador', 
                  'quem_solicitou', 
                  'quem_autorizou', 
                  'local', 
                  'aeronave', 
                  'usuario'
                  ]
        
        labels = {
            'usuario': '',
        }
        
        widgets = {'usuario': forms.HiddenInput(),
                   'titulo': forms.TextInput(attrs={'class': 'form-control'}),
                   'concluida': forms.HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['aeronave'].queryset = Aeronave.objects.filter(em_uso=False)
        self.fields['titulo'].widget.attrs.update({
            'placeholder': 'Informe um título para operação'
        })
        self.fields['quem_autorizou'].widget.attrs.update({
            'placeholder': 'Informe quem autorizou a operação'
        })
        self.fields['quem_solicitou'].widget.attrs.update({
            'placeholder': 'Informe quem solicitou a operação'
        })
        self.fields['aeronave'].widget.attrs.update({
            'class': 'aeronave_escolha'
        })
        
        campos = ['titulo', 
                  'piloto_observador', 
                  'quem_solicitou',
                  'quem_autorizou', 
                  'local', 
                  'aeronave', 
                  'usuario']
        
        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')
            
    
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
            'local', 'arquivo_solicitacao',
            'num_sarpas', 'opm_apoiada',
            'unidade_apoiada', 'natureza_de_voo',
            'tipo_de_operacao', 'aeronave',
            'relato_da_missao',
        ]
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
            'relato_da_missao': 'Relato da missão',
            'data': 'Data inicial',
            'data_final': 'Data final'
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

        self.fields['arquivo_solicitacao'].widget.attrs.update({
            'class': 'p-3',
            'accept': "application/pdf", 
        })

                
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
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')


class AeronavesForm(forms.ModelForm):

    class Meta:
        model = Aeronave
        fields = ['prefixo', 'modelo',
                  'marca', 'local',
                  'em_uso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        campos = ['prefixo', 'modelo', 'marca', 'local', 'em_uso']

        for campo in campos:
            adiciona_atributo_classe_ao_widget(self, campo, campo, 'form-control')


class AeronaveSelectForm(forms.Form):
    aeronave = forms.ModelChoiceField(queryset=Aeronave.objects.all(), empty_label='Selecione uma aeronave')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['aeronave'].widget.attrs.update({'class': 'form-control aircraft_selection_form'})
        
        
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
        
        fields = [
            'piloto', 'aeronave',
            'num_helices', 'num_baterias',
            'baterias_carregadas', 'bateria_controle_carregada',
            'corpo', 'hastes_motor',
            'helices', 'gimbal',
            'holofote', 'auto_falante',
            'luz_estroboscopica', 'cabos',
            'carregador', 'fonte',
            'smart_controller', 'controle',
            'cartao_sd', 'IMU',
            'compass', 'sinal_transmissao',
            'sistema_rtk_ppk', 'sinal_de_video',
            'telemetria', 'paraquedas',
            'alteracoes']

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


        