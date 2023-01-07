from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services
from apps.cortex.models import PersonCortex
from . import models

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


@shared_task(bind=True)
def cortex_consult(self, username, person, cpf=False, name=False, mother_name=False, birthdate=False, nickname=False):
    """
    Get service and consult person on cortex by params
    """
    try:
        print('TASKS person')
        data = portalCortexService.get_person_by_cpf(cpf=cpf, username=username)

        if data:
            cortex_instance, created = PersonCortex.objects.update_or_create(**data)
            if cortex_instance:
                models.Registry.objects.update_or_create(system_label="CORTEX PESSOA", system_uuid=cortex_instance.uuid, person=person)
            else:
                logger.warn('Cortex instance not valid - {}'.format(cortex_instance))            
        else:
            logger.warn('Data not valid - {}'.format(data))
    except Exception as e:
        logger.error('Error while getting registry in cortex - {}'.format(e))
