import re
from django.conf import settings
from django.core.exceptions import ValidationError


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