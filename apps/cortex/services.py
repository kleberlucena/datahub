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
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/pessoas/cpf/{cpf}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_person_by_cpf')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_person_by_cpf - {}'.format(e))
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
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/pessoas/nascimento/?name={name}&birthdate={birthdate}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get person by birthdate')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_person_by_birthdate - {}'.format(e))
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
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/pessoas/mae/?name={name}&mother_name={mother_name}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_person_by_mother_name')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_person_by_mother_name - {}'.format(e))
        finally:
            return data

    def get_person_bnmp_by_cpf(self, username, cpf):
        """
        Get person bnmp register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/bnmp/cpf/{cpf}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_bnmp_by_cpf')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_bnmp_by_cpf - {}'.format(e))
        finally:
            return data

    def get_person_bnmp_by_mother(self, username, name, mother_name):
        """
        Get person bnmp register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/bnmp/mae/listagem/?name={name}&mother_name={mother_name}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_bnmp_by_mother')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_bnmp_by_mother - {}'.format(e))
        finally:
            return data

    def get_person_bnmp_by_birthdate(self, username, name, birthdate):
        """
        Get person bnmp register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/bnmp/nascimento/listagem/?name={name}&birthdate={birthdate}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_bnmp_by_birthdate')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_bnmp_by_birthdate - {}'.format(e))
        finally:
            return data

    def get_person_bnmp_by_nickname(self, username, nickname):
        """
        Get person bnmp register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/bnmp/alcunha/listagem/?nickname={nickname}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_bnmp_by_nickname')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_bnmp_by_nickname - {}'.format(e))
        finally:
            return data

    def get_person_bnmp_by_name_nickname(self, username, name, nickname):
        """
        Get person bnmp register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/bnmp/nomealcunha/listagem/?name={name}&nickname={nickname}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_bnmp_by_name_and_nickname')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_bnmp_by_name_and_nickname - {}'.format(e))
        finally:
            return data

    def get_person_bnmp_by_name(self, username, name):
        """
        Get person bnmp register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/bnmp/nome/listagem/?name={name}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_bnmp_by_name')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_bnmp_by_name - {}'.format(e))
        finally:
            return data

    def get_bnmp_by_idpessoa(self, username, idpessoa):
        """
        Get person bnmp register from API on CORTEX
        :return: json with person data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/bnmp/{idpessoa}", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while getting person in get_bnmp_by_id')
        except Exception as e:
            data = None
            logger.error('Error while getting person in get_bnmp_by_id - {}'.format(e))
        finally:
            return data

    def get_city_by_placa(self, placa, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/municipios/{placa}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request cities from get_city_by_placa')
        except Exception as e:
            data = None
            logger.error('Error while request cities from get_city_by_placa - {}'.format(e))
        finally:
            return data

    def get_vehicle_by_placa(self, placa, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/placa/{placa}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request vehicle from get_vehicle_by_placa')
        except Exception as e:
            data = None
            logger.error('Error while request vehicle from get_vehicle_by_placa - {}'.format(e))
        finally:
            return data
        
    def get_vehicle_by_renavam(self, renavam, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/renavam/{renavam}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request vehicle from get_vehicle_by_renavam')
        except Exception as e:
            data = None
            logger.error('Error while request vehicle from get_vehicle_by_renavam - {}'.format(e))
        finally:
            return data
        
    def get_vehicle_by_proprietario(self, cpf, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/proprietario/{cpf}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request vehicle from get_vehicle_by_proprietario')
        except Exception as e:
            data = None
            logger.error('Error while request vehicle from get_vehicle_by_proprietario - {}'.format(e))
        finally:
            return data
        
    def get_vehicle_by_possuidor(self, cpf, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/possuidor/{cpf}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request vehicle from get_vehicle_by_possuidor')
        except Exception as e:
            data = None
            logger.error('Error while request vehicle from get_vehicle_by_possuidor - {}'.format(e))
        finally:
            return data
        
    def get_vehicle_by_motor(self, motor, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/motor/{motor}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request vehicle from get_vehicle_by_motor')
        except Exception as e:
            data = None
            logger.error('Error while request vehicle from get_vehicle_by_motor - {}'.format(e))
        finally:
            return data
        
    def get_vehicle_by_cambio(self, cambio, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/cambio/{cambio}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request vehicle from get_vehicle_by_cambio')
        except Exception as e:
            data = None
            logger.error('Error while request vehicle from get_vehicle_by_cambio - {}'.format(e))
        finally:
            return data
        
    def get_vehicle_by_chassi(self, chassi, username):
        """
        Get vehicle register from API on CORTEX
        :return: json with vehicle data
        """
        headers = {
            'Content-Type': content_type,
            'Authorization': f'Token {authorization}',
            'username': username
        }
        data = None
        try:
            response = requests.get(f"{portal_url_base}/api/v1/cortex/veiculos/chassi/{chassi}/", headers=headers, timeout=(50))
            data = json.loads(response.content)
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout while request vehicle from get_vehicle_by_chassi')
        except Exception as e:
            data = None
            logger.error('Error while request vehicle from get_vehicle_by_chassi - {}'.format(e))
        finally:
            return data