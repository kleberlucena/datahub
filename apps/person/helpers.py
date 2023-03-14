import logging
import uuid

from apps.document.models import Document
from apps.cortex import helpers
from . import models
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_external_consult(username, cpf=None):
    # TODO: substituir person.documents.all por Ducments.objects.filter(number=cpf)
    try:
        return helpers.process_cortex_consult(username, cpf)        
    except Exception as e:
        logger.warn('Attention, problem while get cortex person and registry on bacinf - {}'.format(e))
        return None

def process_update_registers(id_person, username, cpf=None):
    try:
        person_cortex = helpers.process_cortex_consult(username, cpf)
        if person_cortex:
            documents = models.Person.objects.get(id=id_person).documents.all()
            helpers.update_registers(documents=documents, person_cortex=person_cortex)
    except Exception as e:
        logger.warn('Attention, problem while update person cortex registry on bacinf - {}'.format(e))