import logging
import uuid

from apps.document.models import Document
from apps.cortex import helpers
from . import models
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_external_consult(id_person, username, cpf=None):
    # TODO: validar atributos do usuário
    person_cortex = helpers.process_cortex_consult(username, cpf)
    if person_cortex:
        person = models.Person.objects.get(id=id_person)
        helpers.update_registers(documents=person.documents.all(), person_cortex=person_cortex)
    """ try:
        if cpf:
            person_cortex = PersonCortex.objects.filter(numeroCPF=cpf)
            person = models.Person.objects.get(id=id_person)
            tasks.cortex_consult(username=username, person=person, cpf=cpf)
        else:
            logger.warn('CPF not informed or invalid - {}'.format(cpf))
    except (ValueError, models.Person.DoesNotExist):
        logger.error('Error while getting person - {}'.format(ValueError))
    except Exception as e:
        logger.error('Error while processing helper in app person - {}'.format(e)) """


""" def validate_document(number):
    try:
        document = Document.objects.get(number=number)
        return document
    except Document.DoesNotExist:
        return None
    except Exception as e:
        logger.error('Error while getting document in bacinf - {}'.format(e))
        return None """