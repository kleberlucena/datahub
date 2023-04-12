import logging
import uuid
from datetime import date

from apps.document.models import Document
from apps.cortex import helpers
from apps.cortex.models import PersonCortex
from apps.cortex import tasks as tasks_cortex
from apps.bnmp.models import PersonBNMP
from apps.bnmp import tasks as tasks_bnmp
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

def process_cortex_consult(username, cpf=None):
    try:
        cortex_person = PersonCortex.objects.get(numeroCPF=cpf)
        if cortex_person.updated_at.date() < date.today():
            tasks_cortex.cortex_update(username, cortex_person).delay()
    except PersonCortex.DoesNotExist:       
        try:          
            tasks_cortex.cortex_consult(username=username, cpf=cpf).delay()
        except Exception as e:
            logger.error('Error while get person_cortex in cortex_server - {}'.format(e))
    except Exception as e:
        logger.error('Error while update person_cortex in cortex_server - {}'.format(e))

def process_bnmp_consult(username, cpf=None):
    try:
        person_bnmp = PersonBNMP.objects.get(numeroCPF=cpf)
        if person_bnmp.updated_at.date() < date.today():
            tasks_bnmp.bnmp_update(username, person_bnmp=person_bnmp).delay()
    except PersonBNMP.DoesNotExist:       
        try:          
            tasks_bnmp.bnmp_consult(username=username, cpf=cpf).delay()
        except Exception as e:
            logger.error('Error while get person_bnmp in cortex_server - {}'.format(e))
    except Exception as e:
        logger.error('Error while update person_bnmp in cortex_server - {}'.format(e))