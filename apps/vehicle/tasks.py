from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services
from .models import PersonRenavamCortex, VehicleCortex, RegistryVehicleCortex

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


@shared_task(bind=True)
def cortex_consult(self, username, placa=False, chassi=False, renavam=False, numeroMotor=False, cpf=False):
    """
    Get service and consult person on cortex by params
    """
    retorno = None
    try:
        logger.info('Task cortex_consult processing')
        vehicle_json = portalCortexService.get_vehicle_by_placa(placa=placa, username=username)
        if vehicle_json:
            del vehicle_json["nomeArrendatario"]
            del vehicle_json["nomePossuidor"]
            del vehicle_json["nomeProprietario"]
            
            arrendatario_json = vehicle_json.pop("arrendatario")
            proprietario_json = vehicle_json.pop("proprietario")
            possuidor_json = vehicle_json.pop("possuidor")

            arrendatario = add_arrendatario(arrendatario_json=arrendatario_json)
            proprietario = add_proprietario(proprietario_json=proprietario_json)
            possuidor = add_possuidor(possuidor_json=possuidor_json)
            
            vehicle_json["dataEmplacamento"] = str(vehicle_json["dataEmplacamento"]) + ".000+0000"
            vehicle_json["dataDeclaracaoImportacao"] = str(vehicle_json["dataDeclaracaoImportacao"]) + ".000+0000"
            
            cortex_instance, created = VehicleCortex.objects.update_or_create(**vehicle_json)

            if proprietario:
               cortex_instance.proprietario = proprietario
            if possuidor:
               cortex_instance.possuidor = possuidor
            if arrendatario:
               cortex_instance.arrendatario = arrendatario
            cortex_instance.save()
            retorno = cortex_instance
            if created:
                logger.info('Created cortex_instance')
            else:
                logger.info('Updated cortex_instance')          
        else:
            logger.warn('Not found vehicle in cortex_consult - {}'.format(placa))
            retorno = None
    except Exception as e:
        logger.error('Error while getting vehicle in cortex_consult - {}'.format(e))
        retorno = None
    finally:
        return retorno

@shared_task(bind=True)
def cortex_update(self, username, vehicle_cortex):
    print("No cortex_update")
    try:
        vehicle_json = portalCortexService.get_vehicle_by_placa(username=username, placa=vehicle_cortex.placa)
        id = vehicle_cortex.id
        if vehicle_json:
            del vehicle_json["nomeArrendatario"]
            del vehicle_json["nomePossuidor"]
            del vehicle_json["nomeProprietario"]
            
            arrendatario_json = vehicle_json.pop("arrendatario")
            proprietario_json = vehicle_json.pop("proprietario")
            possuidor_json = vehicle_json.pop("possuidor")

            arrendatario = add_arrendatario(arrendatario_json=arrendatario_json)
            proprietario = add_proprietario(proprietario_json=proprietario_json)
            possuidor = add_possuidor(possuidor_json=possuidor_json)
            
            vehicle_json["dataEmplacamento"] = str(vehicle_json["dataEmplacamento"]) + ".000+0000"
            vehicle_json["dataDeclaracaoImportacao"] = str(vehicle_json["dataDeclaracaoImportacao"]) + ".000+0000"
            
            cortex_instance, created = VehicleCortex.objects.update_or_create(id=id, defaults={**vehicle_json})
            
            if proprietario:
               cortex_instance.proprietario = proprietario
            if possuidor:
               cortex_instance.possuidor = possuidor
            if arrendatario:
               cortex_instance.arrendatario = arrendatario
            cortex_instance.save()
            retorno = cortex_instance
            if created:
                logger.info('Created cortex_instance')
            else:
                logger.info('Updated cortex_instance')          
        else:
            logger.warn('Not found vehicle in cortex_update - {}'.format(vehicle_cortex.placa))
            retorno = None
    except Exception as e:
        logger.error('Error while getting vehicle in cortex_consult - {}'.format(e))
        retorno = None
    finally:
        return retorno
    
def add_arrendatario(arrendatario_json):
    try:
        if arrendatario_json["id"] == 0 or arrendatario_json["id"] == None:
             return None
        else:
            person, created = PersonRenavamCortex.objects.update_or_create(
                id = arrendatario_json["id"],
                tipoDocumento = arrendatario_json["tipoDocumentoArrendatario"],
                numeroDocumento = arrendatario_json["numeroDocumentoArrendatario"],
                nome = arrendatario_json["nomeArrendatario"],
                endereco = arrendatario_json["enderecoArrendatario"]
            )
            return person
    except Exception as e:
        logger.error('Error while add arrendatario vehicle from cortex - {}'.format(e))
        return None
    
def add_proprietario(proprietario_json):
    try:
        if proprietario_json["id"] == 0 or proprietario_json["id"] == None:
             return None
        else:
            person, created = PersonRenavamCortex.objects.update_or_create(
                id = proprietario_json["id"],
                tipoDocumento = proprietario_json["tipoDocumentoProprietario"],
                numeroDocumento = proprietario_json["numeroDocumentoProprietario"],
                nome = proprietario_json["nomeProprietario"],
                endereco = proprietario_json["enderecoProprietario"]
            )
            return person
    except Exception as e:
        logger.error('Error while add proprietario vehicle from cortex - {}'.format(e))
        return None
    
def add_possuidor(possuidor_json):
    try:
        if possuidor_json["id"] == 0 or possuidor_json["id"] == None:
             return None
        else:
            person, created = PersonRenavamCortex.objects.update_or_create(
                id = possuidor_json["id"],
                tipoDocumento = possuidor_json["tipoDocumentoPossuidor"],
                numeroDocumento = possuidor_json["numeroDocumentoPossuidor"],
                nome = possuidor_json["nomePossuidor"],
                endereco = possuidor_json["enderecoPossuidor"]
            )
            return person
    except Exception as e:
        logger.error('Error while add possuidor vehicle from cortex - {}'.format(e))
        return None
