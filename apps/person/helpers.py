import logging

from apps.document.models import Document
from . import tasks
from . import models

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_external_consult(person, username, cpf=None):
    # TODO: validar atributos do usuário
    if cpf:
        try:
            retorno = tasks.cortex_consult(username=username, cpf=cpf)
            models.Registry.objects.update_or_create(system_label="CORTEX", system_uuid=retorno.uuid, person=person)
        except Exception as e:
            logger.error('Error while getting registry in cortex - {}'.format(e))
    else:
        logger.info('CPF not informed or invalid - {}'.format(cpf))


def validate_document(number):
    try:
        document = Document.objects.get(number=number)
        return document
    except Document.DoesNotExist:
        return None
    except Exception as e:
        logger.error('Error while getting document in bacinf - {}'.format(e))
        return None