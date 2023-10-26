from apps.rpa_manager.forms import ChecklistForm
from apps.rpa_manager.models import AicraftHistoric

def saveNewChecklistInAircraftHistoric(request, initial_data):
    checklist_form = ChecklistForm(request, initial=initial_data)
    checklist = checklist_form.save(commit=False)
    
    AicraftHistoric.objects.create(
        aeronave=checklist.aeronave,
        num_helices = checklist.num_helices,  
        num_baterias = checklist.num_baterias, 
        baterias_carregadas = checklist.baterias_carregadas, 
        bateria_controle_carregada = checklist.bateria_controle_carregada, 
        corpo = checklist.corpo, 
        hastes_motor = checklist.hastes_motor, 
        helices = checklist.helices, 
        gimbal = checklist.gimbal, 
        holofote = checklist.holofote, 
        auto_falante = checklist.auto_falante, 
        luz_estroboscopica= checklist.luz_estroboscopica, 
        cabos = checklist.cabos, 
        carregador = checklist.carregador, 
        fonte = checklist.fonte, 
        smart_controller = checklist.smart_controller, 
        controle = checklist.controle, 
        cartao_sd = checklist.cartao_sd, 
        IMU = checklist.IMU, 
        compass = checklist.compass, 
        sinal_transmissao = checklist.sinal_transmissao, 
        sistema_rtk_ppk = checklist.sistema_rtk_ppk, 
        sinal_de_video = checklist.sinal_de_video, 
        telemetria = checklist.telemetria, 
        paraquedas = checklist.paraquedas,                
        alteracoes = checklist.alteracoes
    )
    