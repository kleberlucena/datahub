import pytz
from datetime import datetime
from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services
from .models import PersonRenavamCortex, VehicleCortex, RegistryVehicleCortex
from apps.person.models import Person
from apps.person.models import Person

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


def update_registers(person_renavam_cortex):
    try:
        people = Person.objects.filter(
            documents__number__icontains=person_renavam_cortex.numeroDocumento)
        if people:
            for person in people:
                RegistryVehicleCortex.objects.update_or_create(
                    person_renavam_cortex=person_renavam_cortex, person=person)
    except Exception as e:
        logger.error(
            'Error while update or create Registry vehicle_cortex - {}'.format(e))


@shared_task(bind=True)
def cortex_consult_vehicle_by_cpf(self, username, cpf):
    vehicles_json = None
    retorno = None
    try:
        vehicles_json = portalCortexService.get_vehicle_by_proprietario(
            cpf=cpf, username=username)
    except Exception as e:
        logger.error(
            'Error while getting vehicles_cortex by CPF - {}'.format(e))
    try:
        if isinstance(vehicles_json, dict):
            retorno = add_vehicle(vehicle_json=vehicles_json)
        elif isinstance(vehicles_json, list):
            retorno = []
            for item in vehicles_json:
                retorno.append(add_vehicle(vehicle_json=item))
    except Exception as e:
        logger.error('Error while add vehicles_cortex by CPF - {}'.format(e))
    finally:
        return retorno


@shared_task(bind=True)
def cortex_consult(self, username, placa=False, chassi=False, renavam=False, motor=False):
    """
    Get service and consult person on cortex by params
    """
    vehicle_json = None
    retorno = None
    try:
        logger.info('Task cortex_consult processing')
        if placa:
            vehicle_json = portalCortexService.get_vehicle_by_placa(
                placa=placa, username=username)
        elif chassi:
            vehicle_json = portalCortexService.get_vehicle_by_chassi(
                chassi=chassi, username=username)
        elif renavam:
            vehicle_json = portalCortexService.get_vehicle_by_renavam(
                renavam=renavam, username=username)
        elif motor:
            vehicle_json = portalCortexService.get_vehicle_by_motor(
                motor=motor, username=username)
    except Exception as e:
        logger.error(
            'Error while getting vehicle_cortex by portal service in cortex_consult - {}'.format(e))
    try:
        if isinstance(vehicle_json, dict):
            retorno = add_vehicle(vehicle_json=vehicle_json)
        elif isinstance(vehicle_json, list):
            retorno = []
            for item in vehicle_json:
                retorno.append(add_vehicle(vehicle_json=item))
    except Exception as e:
        logger.error(
            'Error while getting vehicle_cortex by portal service in cortex_consult - {}'.format(e))
    finally:
        return retorno


@shared_task(bind=True)
def cortex_update(self, username, vehicle_cortex):
    try:
        vehicle_json = portalCortexService.get_vehicle_by_placa(
            username=username, placa=vehicle_cortex.placa)
        retorno = update_vehicle(
            vehicle_json=vehicle_json, id=vehicle_cortex.id)
    except Exception as e:
        logger.error(
            'Error while getting vehicle in cortex_consult - {}'.format(e))
        retorno = None
    finally:
        return retorno


def add_arrendatario(arrendatario_json):
    try:
        if arrendatario_json["id"] == 0 or arrendatario_json["id"] == None:
            return None
        else:
            person = None
            try:
                person = PersonRenavamCortex.objects.get(
                    id=arrendatario_json["id"])
            except PersonRenavamCortex.DoesNotExist:
                person = PersonRenavamCortex.objects.create(
                    id=arrendatario_json["id"],
                    tipoDocumento=arrendatario_json["tipoDocumentoArrendatario"],
                    numeroDocumento=arrendatario_json["numeroDocumentoArrendatario"],
                    nome=arrendatario_json["nomeArrendatario"],
                    endereco=arrendatario_json["enderecoArrendatario"]
                )
                update_registers(person_renavam_cortex=person)
            return person
    except Exception as e:
        logger.error(
            'Error while add arrendatario vehicle from cortex - {}'.format(e))
        return None


def add_proprietario(proprietario_json):
    try:
        if proprietario_json["id"] == 0 or proprietario_json["id"] == None:
            return None
        else:
            person = None
            try:
                person = PersonRenavamCortex.objects.get(
                    id=proprietario_json["id"])
            except PersonRenavamCortex.DoesNotExist:
                person = PersonRenavamCortex.objects.create(
                    id=proprietario_json["id"],
                    tipoDocumento=proprietario_json["tipoDocumentoProprietario"],
                    numeroDocumento=proprietario_json["numeroDocumentoProprietario"],
                    nome=proprietario_json["nomeProprietario"],
                    endereco=proprietario_json["enderecoProprietario"]
                )
                update_registers(person_renavam_cortex=person)
            return person
    except Exception as e:
        logger.error(
            'Error while add proprietario vehicle from cortex - {}'.format(e))
        return None


def add_possuidor(possuidor_json):
    try:
        if possuidor_json["id"] == 0 or possuidor_json["id"] == None:
            return None
        else:
            person = None
            try:
                person = PersonRenavamCortex.objects.get(
                    id=possuidor_json["id"])
            except PersonRenavamCortex.DoesNotExist:
                person, created = PersonRenavamCortex.objects.create(
                    id=possuidor_json["id"],
                    tipoDocumento=possuidor_json["tipoDocumentoPossuidor"],
                    numeroDocumento=possuidor_json["numeroDocumentoPossuidor"],
                    nome=possuidor_json["nomePossuidor"],
                    endereco=possuidor_json["enderecoPossuidor"]
                )
                update_registers(person_renavam_cortex=person)
            return person
    except Exception as e:
        logger.error(
            'Error while add possuidor vehicle from cortex - {}'.format(e))
        return None


def add_vehicle(vehicle_json):
    arrendatario = None
    proprietario = None
    possuidor = None
    timezone = pytz.timezone('America/Sao_Paulo')
    try:
        if vehicle_json:
            del vehicle_json['nomeArrendatario']
            del vehicle_json['nomePossuidor']
            del vehicle_json['nomeProprietario']

            arrendatario_json = vehicle_json.pop('arrendatario')
            proprietario_json = vehicle_json.pop('proprietario')
            possuidor_json = vehicle_json.pop('possuidor')

            proprietario = add_proprietario(
                proprietario_json=proprietario_json)
            possuidor = add_possuidor(possuidor_json=possuidor_json)
            arrendatario = add_arrendatario(
                arrendatario_json=arrendatario_json)
    except Exception as e:
        logger.error(
            'Error while adapt proprietario, possuidor e arrendatario in cortex_consult - {}'.format(e))

    # try:
    #     if vehicle_json:
    #         # dt = timezone.localize(datetime(2019, 9, 13, 0, 0, 0))
    #         # vehicle_json['dataAtualizacaoVeiculo'] = str(vehicle_json['dataAtualizacaoVeiculo']) + ".000+0000"
    #         vehicle_json['dataEmissaoCRLV'] = str(vehicle_json['dataEmissaoCRLV']) + ".000+0000"
    #         vehicle_json['dataReplicacao'] = str(vehicle_json['dataReplicacao']) + ".000+0000"
    #         # vehicle_json['dataEmplacamento'] = str(vehicle_json['dataEmplacamento']) + ".000+0000"
    #         vehicle_json['dataEmplacamento'] = str(vehicle_json['dataEmplacamento']) + ".000+0000"
    #         # vehicle_json['dataDeclaracaoImportacao'] = str(vehicle_json['dataDeclaracaoImportacao']) + ".000+0000"
    #         # vehicle_json['dataDeclaracaoImportacao'] = str(vehicle_json['dataDeclaracaoImportacao']) + ".000+0000"
    # except Exception as e:
    #     logger.error('Error while convert dataEmplacamento e dataDeclaracaoImportacao to json from vehicle model field - {}'.format(e))

    try:
        if vehicle_json:
            id = vehicle_json["id"]
            cortex_instance, created = VehicleCortex.objects.update_or_create(
                id=id, defaults={**vehicle_json})

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
            logger.warn('Not found vehicle in cortex_consult ')

    except Exception as e:
        logger.error(
            'Error while save vehicle in cortex_consult - {}'.format(e))
    finally:
        return retorno


def update_vehicle(vehicle_json, id):
    try:
        del vehicle_json["nomeArrendatario"]
        del vehicle_json["nomePossuidor"]
        del vehicle_json["nomeProprietario"]
        arrendatario_json = vehicle_json.pop("arrendatario")
        proprietario_json = vehicle_json.pop("proprietario")
        possuidor_json = vehicle_json.pop("possuidor")
        proprietario = add_proprietario(proprietario_json=proprietario_json)
        possuidor = add_possuidor(possuidor_json=possuidor_json)
        arrendatario = add_arrendatario(arrendatario_json=arrendatario_json)
        # vehicle_json['dataEmissaoCRLV'] = str(vehicle_json['dataEmissaoCRLV']) + ".000+0000"
        # vehicle_json['dataReplicacao'] = str(vehicle_json['dataReplicacao']) + ".000+0000"
        # vehicle_json["dataEmplacamento"] = str(vehicle_json["dataEmplacamento"]) + ".000+0000"

        cortex_instance, created = VehicleCortex.objects.update_or_create(
            id=id, defaults={**vehicle_json})
        if proprietario:
            cortex_instance.proprietario = proprietario
        if possuidor:
            cortex_instance.possuidor = possuidor
        if arrendatario:
            cortex_instance.arrendatario = arrendatario
        cortex_instance.save()
        if created:
            logger.info('Created cortex_instance')
        else:
            logger.info('Updated cortex_instance')
        return cortex_instance
    except Exception as e:
        logger.error(
            'Error while update vehicle_cortex by cortex_consult - {}'.format(e))
        return None
