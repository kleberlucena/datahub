from django.conf import settings
import requests
import json
import logging
import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)

portal_url_base = settings.PORTAL_URL_BASE
content_type = 'application/json'
authorization = settings.PORTAL_TOKEN


class PortalCortexService(object):

    def get_person_by_cpf(self, cpf, username):
        """
        Get person register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }

        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/pessoas/cpf/{cpf}/", headers=headers, timeout=(5))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_person_by_cpf')
        except Exception as e:
            data = None
            raise logger.error('Error while getting person in get_person_by_cpf - {}'.format(e))
        finally:
            return data

    def get_person_by_birthdate(self, name, birthdate, username):
        """
        Get person register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }

        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/pessoas/nascimento/?name={name}&birthdate={birthdate}", headers=headers, timeout=(5))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_person_by_cpf')
        except Exception as e:
            data = None
            raise logger.error('Error while getting person in get_person_by_cpf - {}'.format(e))
        finally:
            return data

    def get_person_by_mother(self, name, mother_name, username):
        """
        Get person register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }

        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/pessoas/mae/?name={name}&mother_name={mother_name}", headers=headers, timeout=(5))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_person_by_cpf')
        except Exception as e:
            data = None
            raise logger.error('Error while getting person in get_person_by_cpf - {}'.format(e))
        finally:
            return data
