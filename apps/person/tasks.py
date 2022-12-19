from celery import shared_task
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services


# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task(bind=True)
def cortex_consult(username, cpf=False, name=False, mother_name=False, birthdate=False, nickname=False):
    """
    Get service and consult person on cortex by params
    """
    services.get_person_by_cpf(cpf=cpf, username=username)

    return
