from billiard.exceptions import TimeLimitExceeded
import json
import logging
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_address_by_zipcode(zipcode):
    # url = settings.URL_ADDRESS_BY_ZIPCODE
    url = f'https://viacep.com.br/ws/{zipcode}/json/'
    content_type = 'application/json'

    try:
        response = requests.get(url, timeout=(15, 180))
        data = json.loads(response.content)
    except requests.exceptions.ReadTimeout:
        logger.warning('get_address_by_zipcode - {}'.format(zipcode))
        data = None
    except TimeLimitExceeded:
        logger.warning('TimeLimitExceeded in zipcode - {}'.format(zipcode))
        data = None
    except Exception as e:
        data = None
        raise logger.error('Error - {} - while getting address in get_address_by_zipcode : {}'.format(e, zipcode))
    finally:
        return data