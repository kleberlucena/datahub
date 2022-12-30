from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services
from apps.cortex.models import PersonCortex

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


@shared_task(bind=True)
def cortex_consult(self, username, cpf=False, name=False, mother_name=False, birthdate=False, nickname=False):
    """
    Get service and consult person on cortex by params
    """
    data = portalCortexService.get_person_by_cpf(cpf=cpf, username=username)

    if data:
        cortex_instance, created = PersonCortex.objects.update_or_create(**data)
        logger.info('PersonCortex - {}'.format(cortex_instance.uuid))
        return cortex_instance
    else:
        return None
