from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
import logging
import requests

from apps.cortex import services
from apps.cortex.models import PersonCortex

self_url_base = settings.SELF_URL_BASE

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


@shared_task(bind=True)
def cortex_consult(self, username, cpf=False, name=False, mother_name=False, birthdate=False, nickname=False):
    """
    Get service and consult person on cortex by params
    """
    data = portalCortexService.get_person_by_cpf(cpf=cpf, username=username)
    print(data)
    if data:
        cortex_instance = PersonCortex.objects.update_or_create(**data)
        print('---------------------------')
        print(cortex_instance.uuid)
        return cortex_instance
    else:
        return None
