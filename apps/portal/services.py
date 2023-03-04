from collections import namedtuple
from django.conf import settings
import logging

import json
from .models import Military, Entity
import time
import requests
# Get an instance of a logger
logger = logging.getLogger(__name__)


def getIBGE():
    api = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/24/municipios"
    requisicao = requests.get(api)

    try:
        lista = requisicao.json()
    except ValueError:
        print("A resposta não chegou com o formato esperado.")

    dicionario = {}
    for indice, valor in enumerate(lista):
        dicionario[indice] = valor

    return dicionario


def convertDictFromObj(dict):
    obj = {
        'url_image': dict['url_image'],
        'admission_date': dict['admission_date'],
        'birthdate': dict['birthdate'],
        'father': dict['father'],
        'mather': dict['mather'],
        'place_of_birth': dict['place_of_birth'],
        'rank': dict['rank'],
        'unit': dict['unit'],
        'nickname': dict['nickname'],
        'activity_status': dict['activity_status'],
        'genre': dict['genre'],
        'email': dict['email'],
        'marital_status': dict['marital_status'],
        'phone': dict['phone'],
        'address': dict['address'],
        'number': dict['number'],
        'complement': dict['complement'],
        'district': dict['district'],
        'city': dict['city'],
        'state': dict['state'],
        'zipcode': dict['zipcode'],
        'register': dict['register'],
        'cpf': dict['cpf'],


    }
    return obj


def get_data_military_api_portal(offset):
    content_type = 'application/json'
    authorization = f'Token {settings.PORTAL_TOKEN}'
    headers = {
        'Content-Type': content_type,
        'Authorization': authorization
    }
    try:
        data = None
        url = f'{settings.PORTAL_URL_BASE}{settings.PORTAL_RELATIVE_URL_LIST_MILITARY}?limit=10&offset={offset}'
        response = requests.get(url, headers=headers, timeout=(15, 180))
        data = json.loads(response.content)
        print("################################")
        print(data)

    except requests.exceptions.ReadTimeout:
        logger.warning('Timeout while getting get_data_military_api_portal')
    except Exception as e:
        data = None
        raise logger.error(
            'Error while getting get_data_military_api_portal - {}'.format(e))
    finally:
        return data


def get_data_entity_api_portal(offset):
    content_type = 'application/json'
    authorization = f'Token {settings.PORTAL_TOKEN}'
    headers = {
        'Content-Type': content_type,
        'Authorization': authorization
    }
    try:
        data = None
        url = f'{settings.PORTAL_URL_BASE}{settings.PORTAL_RELATIVE_URL_LIST_ENTITY}?limit=10&offset={offset}'
        response = requests.get(url, headers=headers, timeout=(15, 180))
        data = json.loads(response.content)
    except requests.exceptions.ReadTimeout:
        logger.warning('Timeout while getting get_data_entity_api_portal')
    except Exception as e:
        data = None
        raise logger.error('Error while getting get_data_entity_api_portal - {}'.format(e))
    finally:
        return data


