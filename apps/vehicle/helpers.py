import re
import logging
from django.db.models import Q
from datetime import date
from django.core.exceptions import ValidationError

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
    

def process_cortex_movimento_consult(username, placa):
    movimento = None
    try:
        placa = validate_signal(placa)
        if placa:
            movimento = tasks.cortex_consult_movimento(username=username, placa=placa)
        
    except Exception as e:
        logger.error(
            'Error while processing helper movimento in app vehicle - {}'.format(e))
        movimento = None
    finally:
        return movimento


def process_cortex_consult(username, placa=None, chassi=None, renavam=None, motor=None, cambio=None):
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
        elif cambio:
            vehicle_cortex = VehicleCortex.objects.get(numeroCaixaCambio=cambio)

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
            logger.warning('CHEGOU no NotFoundException')
            vehicle_cortex = tasks.cortex_consult(
                username=username, placa=placa, chassi=chassi, renavam=renavam, motor=motor, cambio=cambio)
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

def validate_signal(placa):
    # Remover qualquer formatação adicional da placa
    placa = placa.replace('-', '').replace(' ', '').upper()

    # Expressão regular para verificar a validade da placa
    # Aceita tanto as placas antigas como as do Mercosul
    padrao = r'^([A-Z]{3}\d{4}|[A-Z]{3}\d[A-Z]\d{2})$'

    # Verificar se a placa corresponde ao padrão
    if re.match(padrao, placa):
        return placa
    else:
        raise ValidationError('PLACA inválida', 'invalid')