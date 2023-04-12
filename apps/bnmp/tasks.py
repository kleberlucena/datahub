from celery import shared_task
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
        logger.error('Error while getting document in bacinf helper bnmp - {}'.format(e))
        return None

def update_registers(documents, person_bnmp):
    for document in documents:
        people = document.person_set.all()
        if people:
            for person in people:
                RegistryBNMP.objects.update_or_create(person_bnmp=person_bnmp, person=person)


@shared_task(bind=True)
def bnmp_consult(self, username, cpf=False, name=False, mother_name=False, birthdate=False, nickname=False):
    """
    Get service and consult person on bnmp by params
    """
    # TODO precisa salvar os mandados em banco de dados
    retorno = None
    try:
        logger.info('Task bnmp_consult processing')
        data = portalCortexService.get_person_bnmp_by_cpf(cpf=cpf, username=username)
        print('recuperou a lista')
        user = User.objects.get(username=username)

        if data:
            print(data)
            for item in data:
                bnmp_instance, created = PersonBNMP.objects.update_or_create(**item)
                bnmp_instance.numeroCPF = cpf
                bnmp_instance.created_by = user
                bnmp_instance.save()
                data_mandados = portalCortexService.get_bnmp_by_idpessoa(username=username, idpessoa=bnmp_instance.idpessoa)
                json_mandados = data_mandados['mandadoPrisao']
                if json_mandados is None or len(json_mandados) == 0:
                    logger.info('Without mandadosPrisao')
                else:
                    for item_mandado in json_mandados:
                        print('------------------------------------------')
                        print(item_mandado)
                        mandado_instance, mandado_created = MandadoPrisao.objects.update_or_create(**item_mandado)
                        mandado_instance.create_by = user
                        mandado_instance.person_bnmp=bnmp_instance
                        mandado_instance.save()
                        print(mandado_instance)
                        bnmp_instance.mandados.add(mandado_instance)
                        print('------------------------------------------')
                bnmp_instance.save()
                documents = get_documents(number=cpf)
                update_registers(documents=documents, person_bnmp=bnmp_instance)
                retorno = PersonBNMP.objects.filter(numeroCPF=cpf)
                if created:
                    logger.info('Created bnmp_instance')
                else:
                    logger.info('Updated bnmp_instance')          
        else:
            logger.warn('Not found personbnmp in cortex - {}'.format(cpf))
    except Exception as e:
        logger.error('Error while getting registry in bnmp cortex - {}'.format(e))
    finally:
        return retorno
    
@shared_task(bind=True)
def bnmp_update(username, person_bnmp):
    try:
        idpessoa=person_bnmp.idpessoa
        user = User.objects.get(username=username)
        data_mandados = portalCortexService.get_bnmp_by_idpessoa(username=username, idpessoa=idpessoa)
        if data_mandados:
            print(data_mandados)
            json_mandados = data_mandados['mandadoPrisao']
            if json_mandados is None or len(json_mandados) == 0:
                logger.info('Without mandadosPrisao')
            else:
                for item_mandado in json_mandados:
                    mandado_instance, mandado_created = MandadoPrisao.objects.update_or_create(**item_mandado)
                    mandado_instance.create_by = user
                    mandado_instance.person_bnmp=person_bnmp
                    mandado_instance.save()
                    print(mandado_instance)
                    # bnmp_instance.mandados.append(mandado_instance)
                person_bnmp.save()
                if mandado_created:
                    logger.info('Created bnmp_instance')
                else:
                    logger.info('Updated bnmp_instance')          
        else:
            logger.warn('Not found personbnmp in cortex - {}'.format(idpessoa))
        id = person_bnmp.id
        value = person_json['numeroCPF']
        person_bnmp_updated, created = PersonBNMP.objects.update_or_create(
                    numeroCPF=value, id=id, defaults={**person_json},
                )
        if person_bnmp_updated:
            documents = get_documents(number=person_bnmp_updated.numeroCPF)
            update_registers(documents=documents, person_bnmp=person_bnmp_updated)
            logger.info('Person bnmp updated - {}'.format(person_bnmp_updated.numeroCPF))
    except Exception as e:
        logger.error('Error while getting person in cortex - {}'.format(e))

@shared_task(bind=True)
def bnmp_registry_list(self, username, person_list, cpf):
    person_bnmp = None
    try:
        person_bnmp = PersonBNMP.objects.get(numeroCPF=cpf)
    except PersonBNMP.DoesNotExist:
            logger.warn('Warn, local not exist any person_cortex with this CPF {}'.format(cpf))
            data = portalCortexService.get_person_bnmp_by_cpf(cpf=cpf, username=username)
            if data:
                person_bnmp = PersonBNMP.objects.update_or_create(**data)
            else:
                logger.warn('Warn, cortex not return any person_bnmp')
    try:              
        if(person_bnmp):
            for item in person_list:
                RegistryBNMP.objects.create(person=item, person_bnmp=person_bnmp)
    except Exception as e:
        logger.error('Error while getting person in bnmp - {}'.format(e))