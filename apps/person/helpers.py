import logging
import uuid
from datetime import date

from apps.document.models import Document
from apps.cortex import helpers
from apps.cortex.models import PersonCortex, RegistryCortex
from apps.cortex import tasks as tasks_cortex
from apps.bnmp.models import PersonBNMP, RegistryBNMP
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
        logger.warn(
            'Attention, problem while get cortex person and registry on bacinf - {}'.format(e))
        return None


def process_update_registers(id_person, username, cpf=None):
    try:
        person_cortex = helpers.process_cortex_consult(username, cpf)
        if person_cortex:
            documents = models.Person.objects.get(id=id_person).documents.all()
            helpers.update_registers(
                documents=documents, person_cortex=person_cortex)
    except Exception as e:
        logger.warn(
            'Attention, problem while update person cortex registry on bacinf - {}'.format(e))


def process_cortex_consult(username, cpf, person):
    try:
        person_cortex = PersonCortex.objects.get(numeroCPF=cpf)
        print(person_cortex)
        if person_cortex.updated_at.date() < date.today():
            tasks_cortex.cortex_update.delay(username, person_cortex)
        RegistryCortex.objects.update_or_create(
            person_cortex=person_cortex, person=person)
    except PersonCortex.DoesNotExist:
        try:
            person_cortex = tasks_cortex.cortex_consult.delay(
                username=username, cpf=cpf)
        except Exception as e:
            logger.error(
                'Error while get person_cortex in cortex_server - {}'.format(e))
    except Exception as e:
        logger.error(
            'Error while update person_cortex in cortex_server - {}'.format(e))


def process_bnmp_consult(username, cpf, person):
    try:
        person_bnmp = tasks_bnmp.bnmp_consult.delay(username=username, cpf=cpf)
        print(person_bnmp)
    except Exception as e:
        logger.error(
            'Error while get person_bnmp in cortex_server - {}'.format(e))
