from celery import shared_task
from django.core.exceptions import FieldError
from django.conf import settings
from django.contrib.auth.models import User
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services
from apps.document.models import Document, DocumentType
from apps.bnmp.models import PersonBNMP, MandadoPrisao, RegistryBNMP

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


def get_documents(number):
    try:
        documents = Document.objects.filter(number=number)
        return documents
    except Exception as e:
        logger.error(
            'Error while getting document in bacinf helper bnmp - {}'.format(e))
        return None


def update_registers(documents, person_bnmp):
    for document in documents:
        people = document.person_set.all()
        if people:
            for person in people:
                RegistryBNMP.objects.update_or_create(
                    person_bnmp=person_bnmp, person=person)


@shared_task(bind=True)
def bnmp_consult_idpessoa(self, username, idpessoa):
    retorno = None
    bnmp_instance = None
    mandados = []
    try:
        bnmp_instance = PersonBNMP.objects.get(idpessoa=idpessoa)
    except Exception as e:
        logger.error('Error while getting bnmp in database - {}'.format(e))
        bnmp_instance = None
    try:
        logger.info('Task bnmp_consult_idpessoa processing')

        data_mandados = portalCortexService.get_bnmp_by_idpessoa(
            idpessoa=idpessoa, username=username)

        user = User.objects.get(username=username)
        if bnmp_instance is None and data_mandados is not None:
            new_bnmp_instance = PersonBNMP.objects.create(
                idpessoa=idpessoa,
                nome=data_mandados["nome"],
                alcunha=data_mandados["alcunha"],
                nomeMae=data_mandados["mae"],
                nomePai=data_mandados["pai"],
                dataNascimento=data_mandados["dataNascimento"],
                sexo=data_mandados["sexo"],
                statusPessoa=data_mandados["pessoa"]["statusPessoa"],
                tipoBuscaCPF=data_mandados["tipoBuscaCPF"],
                created_by=user,
            )
            bnmp_instance = new_bnmp_instance
        json_mandados = data_mandados['mandadoPrisao']
        if json_mandados is None or len(json_mandados) == 0:
            logger.info('Without mandadosPrisao')
        else:
            for item_mandado in json_mandados:
                mandado_instance, mandado_created = MandadoPrisao.objects.update_or_create(
                    **item_mandado)
                mandado_instance.create_by = user
                mandado_instance.person_bnmp = bnmp_instance
                mandado_instance.save()
                mandados.append(mandado_instance)
                if bnmp_instance is not None:
                    bnmp_instance.mandados.add(mandado_instance)
            bnmp_instance.save()
        retorno = mandados
    except FieldError as e:
        logger.error(
            'FieldError while getting mandados in bnmp cortex - {}'.format(e))
        raise e
    except Exception as e:
        logger.error(
            'Error while getting mandados in bnmp cortex - {}'.format(e))
    finally:
        return retorno


@shared_task(bind=True)
def bnmp_consult_name_birthdate(self, username, name, birthdate):
    try:
        logger.info('Task bnmp_consult processing')
        data = portalCortexService.get_person_bnmp_by_birthdate(
            name=name, username=username, birthdate=birthdate)
        return data
    except Exception as e:
        logger.error(
            'Error while getting person in bnmp cortex by birthdate - {}'.format(e))
        return None


@shared_task(bind=True)
def bnmp_consult_name_mother(self, username, name, mother_name):
    try:
        logger.info('Task bnmp_consult processing')
        data = portalCortexService.get_person_bnmp_by_mother(
            name=name, username=username, mother_name=mother_name)
        return data
    except Exception as e:
        logger.error(
            'Error while getting person in bnmp cortex by mother - {}'.format(e))
        return None


@shared_task(bind=True)
def bnmp_consult_name_nickname(self, username, name, nickname):
    try:
        logger.info('Task bnmp_consult processing')
        data = portalCortexService.get_person_bnmp_by_nickname(
            name=name, username=username, nickname=nickname)
        return data
    except Exception as e:
        logger.error(
            'Error while getting person in bnmp cortex by name and nickname - {}'.format(e))
        return None


@shared_task(bind=True)
def bnmp_consult_nickname(self, username, nickname):
    try:
        logger.info('Task bnmp_consult processing')
        data = portalCortexService.get_person_bnmp_by_nickname(
            username=username, nickname=nickname)
        return data
    except Exception as e:
        logger.error(
            'Error while getting person in bnmp cortex by nickname - {}'.format(e))
        return None


@shared_task(bind=True)
def bnmp_consult_name(self, username, name):
    try:
        logger.info('Task bnmp_consult processing')
        data = portalCortexService.get_person_bnmp_by_name(
            name=name, username=username)
        return data
    except Exception as e:
        logger.error(
            'Error while getting person in bnmp cortex by name - {}'.format(e))
        return None


@shared_task(bind=True)
def bnmp_consult(self, username, cpf):
    """
    Get service and consult person on bnmp by params
    """
    # TODO precisa salvar os mandados em banco de dados
    retorno = None
    try:
        logger.info('Task bnmp_consult processing')
        data = portalCortexService.get_person_bnmp_by_cpf(
            cpf=cpf, username=username)
        user = User.objects.get(username=username)

        if data:
            for item in data:
                bnmp_instance, created = PersonBNMP.objects.update_or_create(
                    **item)
                bnmp_instance.numeroCPF = cpf
                bnmp_instance.created_by = user
                bnmp_instance.save()
                data_mandados = portalCortexService.get_bnmp_by_idpessoa(
                    username=username, idpessoa=bnmp_instance.idpessoa)
                json_mandados = data_mandados['mandadoPrisao']
                if json_mandados is None or len(json_mandados) == 0:
                    logger.info('Without mandadosPrisao')
                else:
                    for item_mandado in json_mandados:
                        mandado_instance, mandado_created = MandadoPrisao.objects.update_or_create(
                            **item_mandado)
                        mandado_instance.create_by = user
                        mandado_instance.person_bnmp = bnmp_instance
                        mandado_instance.save()
                        bnmp_instance.mandados.add(mandado_instance)
                bnmp_instance.save()
                documents = get_documents(number=cpf)
                update_registers(documents=documents,
                                 person_bnmp=bnmp_instance)
                retorno = PersonBNMP.objects.filter(numeroCPF=cpf)
                if created:
                    logger.info('Created bnmp_instance')
                else:
                    logger.info('Updated bnmp_instance')
        else:
            logger.warn('Not found personbnmp in cortex - {}'.format(cpf))
    except Exception as e:
        logger.error(
            'Error while getting registry in bnmp cortex - {}'.format(e))
    finally:
        return retorno


@shared_task(bind=True)
def bnmp_registry_list(self, username, person_list, cpf):
    person_bnmp = None
    try:
        person_bnmp = PersonBNMP.objects.get(numeroCPF=cpf)
    except PersonBNMP.DoesNotExist:
        logger.warn(
            'Warn, local not exist any person_cortex with this CPF {}'.format(cpf))
        data = portalCortexService.get_person_bnmp_by_cpf(
            cpf=cpf, username=username)
        if data:
            person_bnmp = PersonBNMP.objects.update_or_create(**data)
        else:
            logger.warn('Warn, cortex not return any person_bnmp')
    try:
        if (person_bnmp):
            for item in person_list:
                RegistryBNMP.objects.create(
                    person=item, person_bnmp=person_bnmp)
    except Exception as e:
        logger.error('Error while getting person in bnmp - {}'.format(e))
