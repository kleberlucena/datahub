from . import tasks
from . import models
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_external_consult(person, username, cpf=None):
    # TODO: validar atributos do usu[ario
    if cpf:
        try:
            retorno = tasks.cortex_consult(username=username, cpf=cpf)
            models.Registry.objects.update_or_create(system_label="CORTEX", system_uuid=retorno.uuid, person=person)
        except Exception as e:
            raise logger.error('Error while getting registry in cortex - {}'.format(e))
            print("N'ao encontrado registro no cortex")
    else:
        logger.info('CPF not informed or invalid - {}'.format(cpf))


def validate_document(number):
    try:
        instance = models.Document.objects.filter(number=number)
        return instance
    except:
        return None