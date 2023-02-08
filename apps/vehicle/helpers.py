import logging
from datetime import date

from apps.vehicle.models import VehicleCortex
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_cortex_consult(username, placa=None):
    retorno = None
    try:
        vehicle_cortex = VehicleCortex.objects.get(placa=placa)
        retorno = vehicle_cortex
        if vehicle_cortex.updated_at.date() < date.today():
            logger.info('Request update...')
            vehicle_updated = tasks.cortex_update(username=username, vehicle_cortex=vehicle_cortex)
            if vehicle_updated:
                retorno = vehicle_updated
    except VehicleCortex.DoesNotExist:        
        try:          
            vehicle_cortex = tasks.cortex_consult(username=username, placa=placa)
            if vehicle_cortex:
                retorno = vehicle_cortex
        except Exception as e:
            logger.error('Error while processing DoesnotExist in app vehicle - {}'.format(e))
            retorno = None
    except Exception as e:
            logger.error('Error while processing helper in app vehicle - {}'.format(e))
            retorno = None
    finally:
        return retorno