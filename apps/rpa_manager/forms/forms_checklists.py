from django import forms
from apps.rpa_manager.models import Checklist
from apps.rpa_manager.utils.addAttributes import addAttributes


class ChecklistForm(forms.ModelForm):
    
    ChecklistCheckboxesFields = [
        'batteries_loaded',
        'control_battery_loaded',
        'body',
        'engine_rods',
        'propellers',
        'gimbal',
        'spotlight',
        'load_speaker',
        'stroboscopic_light',
        'cables',
        'charger',
        'smart_controller',
        'controller',
        'sd_card',
        'imu',
        'compass',
        'signal_transmission',
        'system_rtk_ppk',
        'video_signal',
        'telemetry',
        'parachute',
    ]
    
    class Meta:
        model = Checklist
        
        fields = [
            'remote_pilot', 'aircraft',
            'num_propellers', 'num_batteries',
            'batteries_loaded', 'control_battery_loaded',
            'body', 'engine_rods',
            'propellers', 'gimbal',
            'spotlight', 'load_speaker',
            'stroboscopic_light', 'cables',
            'charger', 
            'smart_controller', 'controller',
            'sd_card', 'imu',
            'compass', 'signal_transmission',
            'system_rtk_ppk', 'video_signal',
            'telemetry', 'parachute',
            'changes']

        labels = {
            'remote_pilot': '',
            'num_batteries': 'Número de baterias',
            'num_propellers': 'Número de hélices',
        }
        widgets = {'remote_pilot': forms.HiddenInput()}
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos = ['aircraft', 'num_batteries', 'num_propellers', 'changes']
        
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')
        
        for campo in self.ChecklistCheckboxesFields:
            addAttributes(self, campo, campo, 'checklist_item')
            