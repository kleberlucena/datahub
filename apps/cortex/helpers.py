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
    print('No helper')
    retorno = None
    try:
        retorno = tasks.cortex_consult(username=username, cpf=cpf)
    except Exception as e:
        logger.error('Error while helper consult person in app cortex - {}'.format(e))
    finally:
        return retorno

def update_registers(documents, person_cortex):
    for document in documents:
        people = document.person_set.all()
        if people:
            for person in people:
                models.RegistryCortex.objects.update_or_create(person_cortex=person_cortex, person=person)

def validate_document(number):
    try:
        documents = Document.objects.filter(number=number)
        return documents
    except Exception as e:
        logger.error('Error while getting document in bacinf - {}'.format(e))
        return None

def create_person_and_document(person_cortex):
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
        models.RegistryCortex.objects.create(person_cortex=person_cortex, person=person)

    except Exception as e:
        logger.error('Error while create person and document on bacinf - {}'.format(e))
        return None