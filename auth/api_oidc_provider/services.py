import requests
import json
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class APIKeycloakClient:
    def __init__(self):
        self.access_token = None
        self.username = settings.API_ADMIN_USERNAME
        self.password = settings.API_ADMIN_PASSWORD
        self.keycloak_url = settings.KEYCLOAK_URL
        self.realm = settings.KEYCLOAK_REALM
        self.get_access_token()

    def get_access_token(self):
        """
        Get the access token to requests
        """
        token_url = "{keycloak_url}/realms/master/protocol/openid-connect/token".format(
            keycloak_url=self.keycloak_url,
        )
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = "client_id=admin-cli&username={username}&password={password}&grant_type=password".format(
            username=self.username,
            password=self.password
        )
        response = requests.request(
            "POST", token_url, headers=headers, data=payload)
        data = json.loads(response.content)
        self.access_token = data['access_token']
        # TODO: Remover
        # TODO: Fazer excepção caso esteja offline e enviar mensagem para a tela do sistema
        if not response.status_code == 200:
            logger.error('Unable to get access token')
            return None

# ADMINISTRATION DE GROUPS #######################################
    def update_or_create_group(self, group_name, id_oidc=None):
        """
        Atualizar ou criar um grupo no Keycloak

        Recebe um grupo como string (nome do grupo) e opcionalmente o UUID de identificação do Keycloak se tiver
        persistido no modelo de Entidade do Portal.

        * Se o UUID ou o nome no Keycloak estiver diferente inicia-se o processo de atualização.
        * Se não tiver UUID, checa a existência do grupo com esse nome e obtem o UUID, salvando na tabela de Entidade.
        * Se não tiver nenhum dado no Keycloak sobre o grupo, cria um e persiste o UUID na tabela de Entidade.
        """
        if id_oidc:
            if self.manage_group(group_name, id_oidc):
                return id_oidc
            else:
                self.update_or_create_group(group_name)
        else:
            logger.info(
                'Entity [{}] was requested without id_oidc'.format(group_name))
            group_uuid = self.get_uuid_group_keycloak(group_name)
            if group_uuid:
                group = self.get_group_keycloak(group_uuid)
                return self.manage_group(group['name'], group['id'])
            else:
                logger.info('Entity [{}] will be created'.format(group_name))
                return self.create_group(group_name)

    def manage_group(self, group_name, id_oidc):
        """
        Obtém o grupo pelo UUID e compara com o nome fornecido, solicitando atualização caso haja divergências.
        """
        group = self.get_group_keycloak(id_oidc)
        if group and group['name'] != group_name:
            return self.update_group_keycloak(group_name, id_oidc)
        elif group:
            return group['id']
        else:
            logger.info('Entity [{}] with id_oidc [{}] not found'.format(
                group_name, id_oidc))
            return None

    def create_group(self, group_name):
        """
        Cria um grupo e retorna o UUID do objeto persistido no Keycloak
        """
        url = "{keycloak_url}/admin/realms/{realm}/groups".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "name": group_name,
            "path": "",
            "subGroups": []
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 201:
            id_oidc = self.get_uuid_group_keycloak(group_name)
            logger.info('Entity [{}] was created with the following id_oidc: {}'.format(
                group_name, id_oidc))
            return id_oidc
        elif response.status_code == 401:
            self.get_access_token()
            response2 = self.create_group(group_name)
            return response2
        else:
            logger.error('Entity [{}] was not created. Got status code {} and content {}'.format(
                group_name,
                response.status_code,
                response.content
            ))
            return False

    def get_uuid_group_keycloak(self, group_name):
        """
        Get group id based on name
        return: uuiu or False
        """
        groups = self.get_groups_keycloak()
        for group in groups:
            if group_name == group['name']:
                id_oidc = group['id']
                logger.info('Entity [{}] found with the following {}'.format(
                    group_name, id_oidc))
                return id_oidc
        else:
            logger.info('Entity [{}] was not found'.format(group_name))
            return None

    def get_groups_keycloak(self):
        """
        Get list groups from keycloak
        """
        url = "{keycloak_url}/admin/realms/{realm}/groups".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({})

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            logger.info('The group list was successfully retrieved')
            return json.loads(response.content)
        elif response.status_code == 401:
            self.get_access_token()
            response2 = self.get_groups_keycloak()
            return response2
        else:
            logger.error('The group list was not retrieved')
            return []

    def get_group_keycloak(self, id_oidc):
        """
                Get group from keycloak
                """
        url = "{keycloak_url}/admin/realms/{realm}/groups/{uuid}".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            uuid=id_oidc
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({})

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.content)
        if response.status_code == 401:
            self.get_access_token()
            response2 = self.get_group_keycloak(id_oidc)
            return response2
        else:
            logger.info('Entity with id_oidc [{}] not found'.format(id_oidc))
            logger.info('Status code: {}'.format(response.status_code))
            return None

    def update_group_keycloak(self, group_name, id_oidc):
        """
        Update group in keycloak
        """
        id_oidc = str(id_oidc)

        url = "{keycloak_url}/admin/realms/{realm}/groups/{uuid}".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            uuid=id_oidc
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "id": id_oidc,
            "name": group_name,
            "path": "",
            "subGroups": []
        })

        response = requests.request("PUT", url, headers=headers, data=payload)

        if response.status_code == 204:
            logger.info(
                'Entity [{}] will be updated with id_oidc - {}'.format(group_name, id_oidc))
            return {"id": id_oidc}
        elif response.status_code == 401:
            self.get_access_token()
            response2 = self.update_group_keycloak(group_name, id_oidc)
            return response2
        else:
            logger.error(
                '[{group_name}] - {id_oidc} was not updated. Status_code{status_code} and content {content}'.format(
                    group_name=group_name,
                    id_oidc=id_oidc,
                    status_code=response.status_code,
                    content=response.content
                ))
            return None

    # ADMINISTRATION DE USERS ####################################
    def update_or_create_enjoyer(self, enjoyer, id_oidc=None):
        """
        If it has uuid and the data is different, updade the enjoyer.
        If you don't have uuid, check the existence of a group with the name and retrieve the uuid
        If you don't have anything, create a group
        """
        if id_oidc:
            if self.manage_enjoyer(enjoyer, id_oidc):
                return id_oidc
            else:
                self.update_or_create_enjoyer(enjoyer)
        else:
            logger.info(
                '[update_or_create_enjoyer] - Enjoyer {} was requested without id_oidc'.format(enjoyer.username))
            enjoyer_uuid = self.get_uuid_enjoyer_keycloak(enjoyer.username)
            if enjoyer_uuid:
                enjoyer_data = self.get_enjoyer_keycloak(enjoyer_uuid)
                logger.info(
                    '[update_or_create_enjoyer] - Enjoyer {} data received'.format(enjoyer_data))
                return self.manage_enjoyer(enjoyer, enjoyer_data['id'])
            else:
                logger.info(
                    '[update_or_create_enjoyer] - Enjoyer {} will be created'.format(enjoyer.username))
                return self.create_enjoyer(enjoyer)

    def manage_enjoyer(self, enjoyer, id_oidc):
        """
        If it has uuid and the username is different, updade the enjoyer.
        """
        enjoyer_response = self.get_enjoyer_keycloak(id_oidc)
        if (enjoyer_response and
                ((enjoyer.username != enjoyer_response['username']) or
                 (enjoyer.first_name != enjoyer_response['firstName']) or
                 (enjoyer.last_name != enjoyer_response['lastName']) or
                 (enjoyer.email != enjoyer_response['email']))):
            return self.update_enjoyer_keycloak(enjoyer, enjoyer_response, id_oidc)
        elif enjoyer_response:
            return enjoyer_response['id']
        else:
            logger.info(
                '[manage_enjoyer] - Enployer {} with id_oidc {} not found'.format(enjoyer.username, id_oidc))
            return None

    def get_enjoyer_keycloak(self, id_oidc):
        """
        Get enjoyer from keycloak
        """
        url = "{keycloak_url}/admin/realms/{realm}/users/{uuid}".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            uuid=id_oidc
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({})

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.content)
        if response.status_code == 401:
            self.get_access_token()
            response2 = self.get_enjoyer_keycloak(id_oidc)
            return response2
        else:
            logger.info(
                '[get_enjoyer_keycloak] - Enjoyer with id_oidc [{}] not found'.format(id_oidc))
            logger.info(
                '[get_enjoyer_keycloak] - Status code: {}'.format(response.status_code))
            return None

    def update_enjoyer_keycloak(self, enjoyer, enjoyer_old, id_oidc):
        """
        Update enjoyer in keycloak
        """
        id_oidc = str(id_oidc)
        # If enployer has desable in keycloak the system not will be updated on attribute
        if not enjoyer_old["enabled"]:
            enjoyer.active = False

        url = "{keycloak_url}/admin/realms/{realm}/users/{uuid}".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            uuid=id_oidc
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        try:
            payload = json.dumps({
                "id": id_oidc,
                "username": enjoyer.username,
                "enabled": enjoyer.active,
                "totp": enjoyer_old["totp"],
                "firstName": enjoyer.first_name,
                "lastName": enjoyer.last_name,
                "email": enjoyer.email,
                "emailVerified": enjoyer_old["emailVerified"],
                "createdTimestamp": enjoyer_old["createdTimestamp"],
                "requiredActions": enjoyer_old["requiredActions"],
                # "federatedIdentities": enjoyer_old["federatedIdentities"],
                "notBefore": enjoyer_old["notBefore"],
                "access": {
                    "manageGroupMembership": enjoyer_old["manageGroupMembership"],
                    "view": enjoyer_old["view"],
                    "mapRoles": enjoyer_old["mapRoles"],
                    "impersonate": enjoyer_old["impersonate"],
                    "manage": enjoyer_old["manage"]
                }
            })
        except KeyError:
            payload = json.dumps({
                "id": id_oidc,
                "username": enjoyer.username,
                "enabled": enjoyer.active,
                "totp": enjoyer_old["totp"],
                "firstName": enjoyer.first_name,
                "lastName": enjoyer.last_name,
                "email": enjoyer.email,
            })

        response = requests.request("PUT", url, headers=headers, data=payload)

        if response.status_code == 204:
            logger.info(
                '[update_enjoyer_keycloak] - Enjoyer {} will be updated with id_oidc - {}'.format(enjoyer.username,
                                                                                                  id_oidc))
            return {"id": id_oidc}
        elif response.status_code == 401:
            self.get_access_token()
            response2 = self.update_enjoyer_keycloak(
                enjoyer, enjoyer_old, id_oidc)
            return response2
        else:
            logger.error(
                '[update_enjoyer_keycloak] - [{username}] - {id_oidc} was not updated. Status_code{status_code} and content {content}'.format(
                    username=enjoyer.username,
                    id_oidc=id_oidc,
                    status_code=response.status_code,
                    content=response.content
                ))
            return None

    def get_uuid_enjoyer_keycloak(self, username):
        """
        Get enjoyser id based on username
        return: uuiu or False
        """
        url = "{keycloak_url}/admin/realms/{realm}/users?username={username}".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            username=str(username)
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({})

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            data = json.loads(response.content)
            if data:
                return data[0]['id']
            else:
                return None
        if response.status_code == 401:
            self.get_access_token()
            response2 = self.get_uuid_enjoyer_keycloak(username)
            return response2
        else:
            logger.info(
                '[get_uuid_enjoyer_keycloak] - Enjoyer with username [{}] not found'.format(username))
            logger.info(
                '[get_uuid_enjoyer_keycloak] - Status code: {}'.format(response.status_code))
            return None

    def create_enjoyer(self, enjoyer):
        """
        Create enjoyer in provider OIDC
        return uuid from enjoyer created or False if enjoyer already exists
        """
        url = "{keycloak_url}/admin/realms/{realm}/users".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "username": enjoyer.username,
            "enabled": True,
            "totp": False,
            "emailVerified": False,
            "firstName": enjoyer.first_name,
            "lastName": enjoyer.last_name,
            "email": enjoyer.email,
            "disableableCredentialTypes": [],
            "requiredActions": [],
            "notBefore": 0,
            "access": {
                "manageGroupMembership": False,
                "view": False,
                "mapRoles": False,
                "impersonate": True,
                "manage": False
            },
            "realmRoles": []
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 201:
            id_oidc = self.get_uuid_enjoyer_keycloak(enjoyer.username)
            logger.info(
                '[create_enjoyer] - Enjoyer {} was created with the following id_oidc: {}'.format(enjoyer.username,
                                                                                                  id_oidc))
            return id_oidc
        elif response.status_code == 401:
            self.get_access_token()
            response2 = self.create_enjoyer(enjoyer)
            return response2
        else:
            logger.error('[create_enjoyer] - Enjoyer {} was not created. Got status code {} and content {}'.format(
                enjoyer.username,
                response.status_code,
                response.content
            ))
            return False

    # UPDATE GROUPS FROM USERS ####################################
    def get_groups_from_user(self, enjoyer_uuid):
        """
        Receive user_uuid e return list from groups uuid
        """
        url = "{keycloak_url}/admin/realms/{realm}/users/{user_uuid}/groups".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            user_uuid=enjoyer_uuid
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({})

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.content)
        if response.status_code == 401:
            self.get_access_token()
            response2 = self.get_groups_from_user(enjoyer_uuid)
            return response2
        else:
            logger.info(
                '[get_groups_from_user] - Groups from enjoyer with uuid {} not found'.format(enjoyer_uuid))
            logger.info(
                '[get_groups_from_user] - Status code: {}'.format(response.status_code))
            return None

    def remove_group_from_user(self, enjoyer_uuid, group_uuid):
        """
        Receive user_uuid e return list from groups uuid
        """
        url = "{keycloak_url}/admin/realms/{realm}/users/{user_uuid}/groups/{group_uuid}".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            user_uuid=enjoyer_uuid,
            group_uuid=group_uuid
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({})

        response = requests.request("DEL", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.content)
        if response.status_code == 401:
            self.get_access_token()
            response2 = self.remove_groups_from_user(enjoyer_uuid, group_uuid)
            return response2
        else:
            logger.info(
                '[remove_group_from_user] - Groups from enjoyer with uuid {} not found'.format(enjoyer_uuid))
            logger.info(
                '[remove_group_from_user] - Status code: {}'.format(response.status_code))
            return None

    def remove_all_groups_from_user(self, enjoyer_uuid):
        groups = self.get_groups_from_user(enjoyer_uuid)
        if groups:
            for group in groups:
                self.remove_group_from_user(enjoyer_uuid, group["id"])
                logger.info('[remove_all_groups_from_user] - Removed group {} from user {}'
                            .format(enjoyer_uuid, group["id"]))

    def remove_all_groups_pmpb_from_user(self, enjoyer_uuid):
        groups = self.get_groups_from_user(enjoyer_uuid)
        if groups:
            for group in groups:
                if group['name'][:5] == 'PMPB|':
                    self.remove_group_from_user(enjoyer_uuid, group["id"])
                    logger.info('[remove_all_groups_pmpb_from_user] - Removed group {} from user {}'
                                .format(enjoyer_uuid, group["id"]))

    def set_group_to_user(self, enjoyer_uuid, group_uuid):
        """
        Receive user_uuid e return list from groups uuid
        """
        url = "{keycloak_url}/admin/realms/{realm}/users/{user_uuid}/groups/{group_uuid}".format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
            user_uuid=enjoyer_uuid,
            group_uuid=group_uuid
        )
        headers = {
            'Authorization': "Bearer {access_token} ".format(
                access_token=self.access_token
            ),
            'Content-Type': 'application/json'
        }
        payload = json.dumps({})

        response = requests.request("PUT", url, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.content)
        if response.status_code == 401:
            self.get_access_token()
            response2 = self.set_group_to_user(enjoyer_uuid, group_uuid)
            return response2
        else:
            logger.info(
                '[set_group_to_user] - Groups with uuid {} not found'.format(enjoyer_uuid))
            logger.info(
                '[set_group_to_user] - Status code: {}'.format(response.status_code))
            return None

    def update_group_pmpb_from_user(self, enjoyer_uuid, new_group_uuid):
        groups_old = self.get_groups_from_user(enjoyer_uuid)
        if groups_old:
            groups_pmpb_quantity = 0
            for group in groups_old:
                if group['name'][:5] == 'PMPB|':
                    groups_pmpb_quantity += 1
                    if group['id'] != new_group_uuid:
                        self.remove_all_groups_pmpb_from_user(enjoyer_uuid)
                        break
            if (groups_pmpb_quantity > 1):
                self.remove_all_groups_pmpb_from_user(enjoyer_uuid)
        self.set_group_to_user(enjoyer_uuid, new_group_uuid)
