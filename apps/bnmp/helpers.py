import re
from django.conf import settings
from django.core.exceptions import ValidationError
import logging
import uuid
from datetime import date

from apps.person.models import Person
from . import models
from . import tasks

# Get an instance of a logger
logger = logging.getLogger(__name__)


INVALIDS_CPFS = ("11111111111", "22222222222", "33333333333", "44444444444", "55555555555",
                 "66666666666", "77777777777", "88888888888", "99999999999", "00000000000")


def digit_generator(cpf, weight):
    sum_digit = 0
    for n in range(weight - 1):
        sum_digit = sum_digit + int(cpf[n]) * weight
        weight = weight - 1

    digit = 11 - sum_digit % 11
    return 0 if digit > 9 else digit


def validate_cpf(value):
    # Extract numbers from string
    cpf = re.sub("[^0-9]", "", value)
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 números', 'invalid')

    # Calculate first validator digit from string
    first_digit = digit_generator(cpf, weight=10)

    # Calculate second validator digit from string
    second_digit = digit_generator(cpf, weight=11)

    # Checks whether the cpf is on the list of invalid persons or if a check digit does not match the digits calculated
    # in the expression
    if cpf in INVALIDS_CPFS or (not cpf[-2:] == f'{first_digit}{second_digit}'):
        raise ValidationError('Número de CPF inválido', 'invalid')
    return cpf


def validate_signal(placa):
    # Remover qualquer formatação adicional da placa
    placa = placa.replace('-', '').replace(' ', '').upper()

    # Expressão regular para verificar a validade da placa
    # Aceita tanto as placas antigas como as do Mercosul
    padrao = r'^([A-Z]{3}\d{4}|[A-Z]{3}\d[A-Z]\d{2})$'

    # Verificar se a placa corresponde ao padrão
    if re.match(padrao, placa):
        return placa
    else:
        raise ValidationError('PLACA inválida', 'invalid')


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
