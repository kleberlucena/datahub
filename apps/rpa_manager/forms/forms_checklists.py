from django import forms
from apps.rpa_manager.models import Checklist
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control

class ChecklistForm(forms.ModelForm):
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
            add_class_and_form_control(self, campo, campo, 'form-control')
        
        for campo in self.camposCheckboxesChecklist:
            add_class_and_form_control(self, campo, campo, 'checklist_item')