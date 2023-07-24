import json
from apps.rpa_manager.models import Aeronave, HistoricoAlteracoesAeronave

# recieve a empty dictionary to be filled with data and returns json
def getLastRegisteredChecklistData(historico_checklist_dict):
    aeronaves = Aeronave.objects.all()
    for aeronave in aeronaves:
        ultimo_registro = HistoricoAlteracoesAeronave.objects.filter(aeronave=aeronave).order_by('-data').first()
        if ultimo_registro:
            historico_checklist_dict[aeronave.id] = {
                'num_helices': str(ultimo_registro.num_helices),
                'num_baterias': str(ultimo_registro.num_baterias),
                'baterias_carregadas': str(ultimo_registro.baterias_carregadas),
                'bateria_controle_carregada': str(ultimo_registro.bateria_controle_carregada),
                'corpo': str(ultimo_registro.corpo),
                'hastes_motor': str(ultimo_registro.hastes_motor),
                'helices': str(ultimo_registro.helices),
                'gimbal': str(ultimo_registro.gimbal),
                'holofote': str(ultimo_registro.holofote),
                'auto_falante': str(ultimo_registro.auto_falante),
                'luz_estroboscopica': str(ultimo_registro.luz_estroboscopica),
                'cabos': str(ultimo_registro.cabos),
                'carregador': str(ultimo_registro.carregador),
                'fonte': str(ultimo_registro.fonte),
                'smart_controller': str(ultimo_registro.smart_controller),
                'controle': str(ultimo_registro.controle),
                'cartao_sd': str(ultimo_registro.cartao_sd),
                'IMU': str(ultimo_registro.IMU),
                'compass': str(ultimo_registro.compass),
                'sinal_transmissao': str(ultimo_registro.sinal_transmissao),
                'sistema_rtk_ppk': str(ultimo_registro.sistema_rtk_ppk),
                'sinal_de_video': str(ultimo_registro.sinal_de_video),
                'telemetria': str(ultimo_registro.telemetria),
                'paraquedas': str(ultimo_registro.paraquedas),
                'alteracoes' : str(ultimo_registro.alteracoes)
            }
        else:
            historico_checklist_dict[aeronave.id] = {
                'num_helices': 4,
                'num_baterias': 4,
                'alteracoes' : 'Sem alteração'
            }

    return json.dumps(historico_checklist_dict)