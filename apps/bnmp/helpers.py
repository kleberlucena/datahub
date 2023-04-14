import logging
import uuid
from datetime import date

from apps.person.models import Person
from . import models
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)

def process_bnmp_consult(username, cpf=None):
    retorno = None
    try:
        print('no helper')
        """ persons_bnmp = models.PersonBNMP.objects.filter(numeroCPF=cpf)
        #if person_bnmp.updated_at.date() < date.today():
        if persons_bnmp is None or len(persons_bnmp) == 0: """
        persons_bnmp = tasks.bnmp_consult(username=username, cpf=cpf)
        """ if persons_bnmp:
            for person_bnmp in persons_bnmp:
                tasks.bnmp_update(username, person_bnmp=person_bnmp) """
        retorno = persons_bnmp
    except Exception as e:
        retorno = None
        logger.error('Error while helper get or update person in app bnmp - {}'.format(e))
    finally:
        return retorno