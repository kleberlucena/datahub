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
        logger.info('Task cortex_consult processing')
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


@shared_task(bind=True)
def cortex_registry_list(self, username, person_list, cpf):
    person_cortex = None
    try:
        person_cortex = PersonCortex.objects.get(numeroCPF=cpf)
    except PersonCortex.DoesNotExist:
            logger.warn('Warn, local not exist any person_cortex with this CPF {}'.format(cpf))
            data = portalCortexService.get_person_by_cpf(cpf=cpf, username=username)
            if data:
                person_cortex = PersonCortex.objects.update_or_create(**data)
            else:
                logger.warn('Warn, cortex not return any person_cortex')
    try:              
        if(person_cortex):
            for item in person_list:
                models.Registry.objects.create(person=item, system_uuid=person_cortex.uuid)
    except Exception as e:
        logger.error('Error while getting person in cortex - {}'.format(e))
    
    