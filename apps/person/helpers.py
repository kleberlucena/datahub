import logging
import uuid

from apps.document.models import Document
from apps.cortex import helpers
from . import models
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_external_consult(id_person, username, cpf=None):
    # TODO: substituir person.documents.all por Ducments.objects.filter(number=cpf)
    person_cortex = helpers.process_cortex_consult(username, cpf)
    if person_cortex:
        person = models.Person.objects.get(id=id_person)
        helpers.update_registers(documents=person.documents.all(), person_cortex=person_cortex)