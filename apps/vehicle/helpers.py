import logging
from datetime import date

from apps.vehicle.models import VehicleCortex
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_cortex_consult(username, placa=None):
    retorno = None
    try:
        print('No helper')
        vehicle_cortex = VehicleCortex.objects.get(placa=placa)
        retorno = vehicle_cortex
        if vehicle_cortex.updated_at.date() < date.today():
            print("tentando atualizar...")
            eita = tasks.cortex_update(username=username, vehicle_cortex=vehicle_cortex)
            print(eita)
            retorno = eita
    except VehicleCortex.DoesNotExist:        
        try:          
            retorno = tasks.cortex_consult(username=username, placa=placa)
        except Exception as e:
            logger.error('Error while processing DoesnotExist in app vehicle - {}'.format(e))
            retorno = None
    except Exception as e:
            logger.error('Error while processing helper in app vehicle - {}'.format(e))
            retorno = None
    finally:
        return retorno