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
    retorno = None
    try:
        cortex_person = models.PersonCortex.objects.get(numeroCPF=cpf)
        retorno = cortex_person
        if cortex_person.updated_at.date() < date.today():
            tasks.cortex_update(username, cortex_person)
    except models.PersonCortex.DoesNotExist:        
        try:          
            retorno = tasks.cortex_consult(username=username, cpf=cpf)
        except Exception as e:
            logger.error('Error while processing helper in app person - {}'.format(e))
            retorno = None
    finally:
        return retorno

def update_registers(documents, person_cortex):
    print(documents)
    for document in documents:
        print('Document - {}'.format( document))
        people = document.person_set.all()
        if people:
            for person in people:
                print('pessoa')
                print(person)
                models.RegistryCortex.objects.update_or_create(person_cortex=person_cortex, person=person)
        else:
            print('Sem pessoas')

def validate_document(number):
    try:
        documents = Document.objects.filter(number=number)
        print('documents: {}'.format(len(documents)))
        return documents
    except Exception as e:
        logger.error('Error while getting document in bacinf - {}'.format(e))
        return None

def create_person_and_document(person_cortex):
    print('aqui')
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
        registry = models.RegistryCortex.objects.create(person_cortex=person_cortex, person=person)
        print(registry.person_cortex)
        for registry in person.registers.all():
            print(registry.uuid)
    except Exception as e:
        logger.error('Error while create person and document on bacinf - {}'.format(e))
        return None