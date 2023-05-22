import logging
from django.db.models import Q
from datetime import date

from apps.vehicle.models import VehicleCortex, PersonRenavamCortex, RegistryVehicleCortex
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_cortex_consult_by_cpf(username, cpf=None):
    try:
        return tasks.cortex_consult_vehicle_by_cpf(username=username, cpf=cpf)
    except Exception as e:
        logger.error('Error while consult vehicle by CPF - {}'.format(e))
        return None


def process_cortex_consult(username, placa=None, chassi=None, renavam=None, motor=None):
    retorno = None
    try:
        vehicle_cortex = None
        if placa:
            vehicle_cortex = VehicleCortex.objects.get(placa=placa)
        elif chassi:
            vehicle_cortex = VehicleCortex.objects.get(chassi=chassi)
        elif renavam:
            vehicle_cortex = VehicleCortex.objects.get(renavam=renavam)
        elif motor:
            vehicle_cortex = VehicleCortex.objects.get(numeroMotor=motor)

        if isinstance(vehicle_cortex, VehicleCortex):
            if vehicle_cortex.updated_at.date() < date.today():
                logger.info('Request vehicle update...')
                vehicle_updated = tasks.cortex_update(
                    username=username, vehicle_cortex=vehicle_cortex)
                if vehicle_updated:
                    vehicle_cortex = vehicle_updated

                if vehicle_cortex.proprietario:
                    tasks.update_registers(vehicle_cortex.proprietario)
                if vehicle_cortex.possuidor:
                    tasks.update_registers(vehicle_cortex.possuidor)
                if vehicle_cortex.arrendatario:
                    tasks.update_registers(vehicle_cortex.arrendatario)

        retorno = vehicle_cortex

    except VehicleCortex.DoesNotExist:
        try:
            print('CHEGOU no NotFoundException')
            vehicle_cortex = tasks.cortex_consult(
                username=username, placa=placa, chassi=chassi, renavam=renavam, motor=motor)
            if vehicle_cortex:
                retorno = vehicle_cortex
        except Exception as e:
            logger.error(
                'Error while processing DoesnotExist in app vehicle - {}'.format(e))
            retorno = None
    except Exception as e:
        logger.error(
            'Error while processing helper in app vehicle - {}'.format(e))
        retorno = None
    finally:
        return retorno
