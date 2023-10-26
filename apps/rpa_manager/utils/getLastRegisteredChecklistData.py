import json
from apps.rpa_manager.models import *

def getLastRegisteredChecklistData(historico_checklist_dict):
    aircrafts = Aircraft.objects.all()
    for aircraft in aircrafts:
        ultimo_registro = AicraftHistoric.objects.filter(aircraft=aircraft).order_by('-date').first()
        if ultimo_registro:
            historico_checklist_dict[f'{aircraft.prefix} - {aircraft.model} - {aircraft.brand}'] = {
                'num_propellers': str(ultimo_registro.num_propellers),
                'num_batteries': str(ultimo_registro.num_batteries),
                'batteries_loaded': str(ultimo_registro.batteries_loaded),
                'control_battery_loaded': str(ultimo_registro.control_battery_loaded),
                'body': str(ultimo_registro.body),
                'engine_rods': str(ultimo_registro.engine_rods),
                'propellers': str(ultimo_registro.propellers),
                'gimbal': str(ultimo_registro.gimbal),
                'spotlight': str(ultimo_registro.spotlight),
                'load_speaker': str(ultimo_registro.load_speaker),
                'stroboscopic_light': str(ultimo_registro.stroboscopic_light),
                'cables': str(ultimo_registro.cables),
                'charger': str(ultimo_registro.charger),
                'smart_controller': str(ultimo_registro.smart_controller),
                'controller': str(ultimo_registro.controller),
                'sd_card': str(ultimo_registro.sd_card),
                'imu': str(ultimo_registro.imu),
                'compass': str(ultimo_registro.compass),
                'signal_transmission': str(ultimo_registro.signal_transmission),
                'system_rtk_ppk': str(ultimo_registro.system_rtk_ppk),
                'video_signal': str(ultimo_registro.video_signal),
                'telemetry': str(ultimo_registro.telemetry),
                'parachute': str(ultimo_registro.parachute),
                'changes' : str(ultimo_registro.changes)
            }
        else:
            historico_checklist_dict[f'{aircraft.prefix} - {aircraft.model} - {aircraft.brand}'] = {
                'num_propellers': 4,
                'num_batteries': 4,
                'changes' : 'Sem alteração'
            }

    return json.dumps(historico_checklist_dict)