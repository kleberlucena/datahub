import logging
import uuid
from datetime import date

from apps.person.models import Person
from . import models
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


def process_bnmp_explorer(username, name=None, nickname=None, mother_name=None, birthdate=None):
    persons_bnmp = None
    try:
        if name:
            if mother_name:
                persons_bnmp = tasks.bnmp_consult_name_mother(
                    username=username, name=name, mother_name=mother_name)
            elif nickname:
                persons_bnmp = tasks.bnmp_consult_name_nickname(
                    username=username, name=name, nickname=nickname)
            elif birthdate:
                persons_bnmp = tasks.bnmp_consult_name_birthdate(
                    username=username, name=name, birthdate=birthdate)
            else:
                persons_bnmp = tasks.bnmp_consult_name(
                    username=username, name=name)
        elif nickname:
            persons_bnmp = tasks.bnmp_consult_nickname(
                username=username, nickname=nickname)
        else:
            persons_bnmp = None
    except Exception as e:
        persons_bnmp = None
        logger.error(
            'Error while helper explore person in app bnmp - {}'.format(e))
    finally:
        return persons_bnmp


def process_bnmp_consult(username, cpf=None):
    retorno = None
    try:
        persons_bnmp = tasks.bnmp_consult(username=username, cpf=cpf)
        retorno = persons_bnmp
    except Exception as e:
        retorno = None
        logger.error(
            'Error while helper get or update person in app bnmp - {}'.format(e))
    finally:
        return retorno


def process_bnmp_idpessoa_consult(username, idpessoa):
    retorno = None
    try:
        mandados_bnmp = tasks.bnmp_consult_idpessoa(
            username=username, idpessoa=idpessoa)
        retorno = mandados_bnmp
    except Exception as e:
        retorno = None
        logger.error(
            'Error while helper get madados_prisao in app bnmp - {}'.format(e))
    finally:
        return retorno
