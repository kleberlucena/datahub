from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services
from apps.cortex.models import PersonCortex
from apps.person.models import Registry

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


@shared_task(bind=True)
def cortex_consult(self, username, cpf=False, name=False, mother_name=False, birthdate=False, nickname=False):
    """
    Get service and consult person on cortex by params
    """
    retorno = None
    try:
        logger.info('Task cortex_consult processing')
        data = portalCortexService.get_person_by_cpf(cpf=cpf, username=username)

        if data:
            cortex_instance, created = PersonCortex.objects.update_or_create(**data)
            retorno = cortex_instance
            if created:
                logger.info('Created cortex_instance')
            else:
                logger.info('Updated cortex_instance')          
        else:
            logger.warn('Not found person in cortex in cortex - {}'.format(cpf))
    except Exception as e:
        logger.error('Error while getting registry in cortex - {}'.format(e))
    finally:
        return retorno

@shared_task(bind=True)
def cortex_update(username, person_cortex):
    try:
        person_json = portalCortexService.get_person_by_cpf(username=username, cpf=person_cortex.numeroCPF)
        id = person_cortex.id
        value = person_json['numeroCPF']
        person_cortex_updated, created = PersonCortex.objects.update_or_create(
                    numeroCPF=value, id=id, defaults={**person_json},
                )
        if person_cortex:
            logger.info('Person cortex updated - {}'.format(cpf))
            return person_cortex_updated
        else:
            return None
    except Exception as e:
        logger.error('Error while getting person in cortex - {}'.format(e))
        return None



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
                Registry.objects.create(person=item, system_uuid=person_cortex.uuid)
    except Exception as e:
        logger.error('Error while getting person in cortex - {}'.format(e))
    
    