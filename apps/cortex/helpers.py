import logging
import uuid
from datetime import date

from apps.document.models import Document, DocumentType
from apps.person.models import Person, Registry
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
            updated = tasks.cortex_update(username, cortex_person)
            if updated:
                retorno = updated
    except models.PersonCortex.DoesNotExist:        
        try:          
            retorno = tasks.cortex_consult(username=username, cpf=cpf)
        except (ValueError, models.Person.DoesNotExist):
            logger.error('Error while getting person - {}'.format(ValueError))
        except Exception as e:
            logger.error('Error while processing helper in app person - {}'.format(e))
    finally:
        return retorno

def update_registers(documents, person_cortex):
    for document in documents:
        print('Document - {}'.format( document))
        people = document.person_set.all()
        if people:
            for person in people:
                print('pessoa')
                print(person)
                Registry.objects.update_or_create(system_label="CORTEX PESSOA", system_uuid=person_cortex.uuid, person=person)
        else:
            print('Sem pessoas')

def validate_document(number):
    try:
        documents = Document.objects.filter(number=number)
        return documents
    except Exception as e:
        logger.error('Error while getting document in bacinf - {}'.format(e))
        return None

def create_person_and_document(person_cortex):
    print('aqui')
    person = Person.objects.create()
    document = Document(number=person_cortex.numeroCPF,
                    name=person_cortex.nomeCompleto,
                    birth_date=person_cortex.dataNascimento,
                    mother=person_cortex.nomeMae,
                    type=DocumentType.objects.get(label="CPF"))
    document.save()
    person.documents.add(document)
    person.save()
    Registry.objects.create(system_label="CORTEX PESSOA", system_uuid=person_cortex.uuid, person=person)