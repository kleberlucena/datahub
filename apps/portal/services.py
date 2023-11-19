import logging
import requests
import urllib.request


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


def get_enjoyer_image_file(image_url):
    try:
        image = urllib.request.urlretrieve(image_url)
    except Exception as e:
        image = None
        logger.error('[SIGPMPB - getMilitaryImageFile] error desconhecido - {}'.format(e))
    finally:
        return image