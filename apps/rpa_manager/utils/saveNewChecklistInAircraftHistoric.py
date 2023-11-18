from apps.rpa_manager.forms import ChecklistForm
from apps.rpa_manager.models import AicraftHistoric

def saveNewChecklistInAircraftHistoric(request, initial_data):
    checklist_form = ChecklistForm(request, initial=initial_data)
    checklist = checklist_form.save(commit=False)
    
    AicraftHistoric.objects.create(
        aircraft=checklist.aircraft,
        num_propellers = checklist.num_propellers,  
        num_batteries = checklist.num_batteries, 
        batteries_loaded = checklist.batteries_loaded, 
        control_battery_loaded = checklist.control_battery_loaded, 
        body = checklist.body, 
        engine_rods = checklist.engine_rods, 
        propellers = checklist.propellers, 
        gimbal = checklist.gimbal, 
        spotlight = checklist.spotlight, 
        load_speaker = checklist.load_speaker, 
        stroboscopic_light= checklist.stroboscopic_light, 
        cables = checklist.cables, 
        charger = checklist.charger, 
        smart_controller = checklist.smart_controller, 
        controller = checklist.controller, 
        sd_card = checklist.sd_card, 
        imu = checklist.imu, 
        compass = checklist.compass, 
        signal_transmission = checklist.signal_transmission, 
        system_rtk_ppk = checklist.system_rtk_ppk, 
        video_signal = checklist.video_signal, 
        telemetry = checklist.telemetry, 
        parachute = checklist.parachute,                
        changes = checklist.changes
    )
    