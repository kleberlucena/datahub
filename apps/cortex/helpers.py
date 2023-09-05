import logging
import uuid
from datetime import date

from apps.document.models import Document, DocumentType
from apps.person.models import Person
from . import models
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_cortex_consult(username, cpf=None):
    try:
        print('aqui process_cortex_consult')
        person_cortex = models.PersonCortex.objects.get(numeroCPF=cpf)
        print(person_cortex)
        if person_cortex.updated_at.date() < date.today():
            person_cortex_updated = tasks.cortex_update(
                username, person_cortex)
            print(person_cortex_updated)
            if person_cortex_updated:
                return person_cortex_updated
        return person_cortex
    except models.PersonCortex.DoesNotExist:
        try:
            person_cortex = tasks.cortex_consult(
                username=username, cpf=cpf)
            return person_cortex
        except Exception as e:
            logger.error(
                'Error while get person_cortex in cortex_server - {}'.format(e))
            return None
    except Exception as e:
        logger.error(
            'Error while update person_cortex in cortex_server - {}'.format(e))
        return None


def update_registers(documents, person_cortex):
    print('aqui update_registers')
    for document in documents:
        people = document.person_set.all()
        if people:
            for person in people:
                models.RegistryCortex.objects.update_or_create(
                    person_cortex=person_cortex, person=person)


def validate_document(number):
    print('aqui validate_document')
    try:
        documents = Document.objects.filter(number=number)
        if documents.exists():
            return documents
        else:
            return None
    except Exception as e:
        logger.error('Error while getting document in bacinf - {}'.format(e))
        return None


def create_person_and_document(person_cortex):
    print('aqui create_person_and_document')
    try:
        person = Person.objects.create()
        document = Document(number=person_cortex.numeroCPF,
                            name=person_cortex.nomeCompleto,
                            birth_date=person_cortex.dataNascimento,
                            mother=person_cortex.nomeMae,
                            type=DocumentType.objects.get(label="CPF"))
        document.save()
        person.documents.add(document)
        person.save()
        models.RegistryCortex.objects.create(
            person_cortex=person_cortex, person=person)

    except Exception as e:
        logger.error(
            'Error while create person and document on bacinf - {}'.format(e))
