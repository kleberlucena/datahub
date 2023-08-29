from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from celery_progress.backend import ProgressRecorder
import logging

from apps.cortex import services
from apps.cortex.models import PersonCortex, RegistryCortex
from apps.portal.models import Military, Entity
from .models import Person, Nickname, Tattoo, Face, Physical

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = services.PortalCortexService()


@shared_task(bind=True)
def cortex_consult(self, username, person, cpf=False, name=False, mother_name=False, birthdate=False, nickname=False):
    """
    Get service and consult person on cortex by params
    """
    try:
        logger.info('Task cortex_consult processing')
        data = portalCortexService.get_person_by_cpf(cpf=cpf, username=username)

        if data:
            cortex_instance, created = PersonCortex.objects.update_or_create(**data)
            if cortex_instance:
                RegistryCortex.objects.update_or_create(person_cortex=cortex_instance, person=person)
            else:
                logger.warn('Cortex instance not valid - {}'.format(cortex_instance))            
        else:
            logger.warn('Data not valid - {}'.format(data))
    except Exception as e:
        logger.error('Error while getting registry in cortex - {}'.format(e))


@shared_task(bind=True)
def cortex_registry_list(self, username, person_list, cpf):
    person_cortex = None
    try:
        person_cortex = PersonCortex.objects.get(numeroCPF=cpf)
    except PersonCortex.DoesNotExist:
        try:
            logger.warn('Warn, local not exist any person_cortex with this CPF {}'.format(cpf))
            data = portalCortexService.get_person_by_cpf(cpf=cpf, username=username)
            if data:
                person_cortex = PersonCortex.objects.update_or_create(numeroCPF=cpf, defaults={**data})
            else:
                logger.warn('Warn, cortex not return any person_cortex')
        except Exception as e:
            logger.error('Error while update person in cortex - {}'.format(e))
    try:              
        if(person_cortex):
            for item in person_list:
                RegistryCortex.objects.create(person=item, person_cortex=person_cortex)
    except Exception as e:
        logger.error('Error while getting person in cortex - {}'.format(e))
    
@shared_task(bind=True)
def task_set_entity_person(self):
    rows = Person.objects.all()
    if rows:
        i = 0
        total = int(rows.count())
        print(total)
        progress_recorder = ProgressRecorder(self)
        for row in rows:
            i += 1
            try:
                user = row.created_by
                entity = row.entity
                # username = User.objects.get(user).username
                # print(username)
                if entity is None:
                    if user:
                        new_entity = Military.objects.get(cpf=user).entity 
                        row.entity = new_entity
                    else:
                        row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                row.save()
            except Exception as e:
                logger.error('Error while update entity person - {}'.format(e))
                if row.entity is None:
                    row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                    row.save()
            finally:
                total_percents = (i / total * 100)
                progress_recorder.set_progress(i, total, f'Concluído {total_percents}%')
    else: 
        progress_recorder.set_progress(0, 0, f'Concluído 100%')

@shared_task(bind=True)
def task_set_entity_nickname(self):
    rows = Nickname.objects.all()
    if rows:
        i = 0
        total = int(rows.count())
        print(total)
        progress_recorder = ProgressRecorder(self)
        for row in rows:
            i += 1
            try:
                user = row.created_by
                entity = row.entity
                if entity is None:
                    if user:
                        new_entity = Military.objects.get(cpf=user).entity 
                        row.entity = new_entity
                    else:
                        row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                row.save()
            except Exception as e:
                logger.error('Error while update entity nickname - {}'.format(e))
                if row.entity is None:
                    row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                    row.save()
            finally:
                total_percents = (i / total * 100)
                progress_recorder.set_progress(i, total, f'Concluído {total_percents}%')
    else: 
        progress_recorder.set_progress(0, 0, f'Concluído 100%')

@shared_task(bind=True)
def task_set_entity_tattoo(self):
    rows = Tattoo.objects.all()
    if rows:
        i = 0
        total = int(rows.count())
        print(total)
        progress_recorder = ProgressRecorder(self)
        for row in rows:
            i += 1
            try:
                user = row.created_by
                entity = row.entity
                if entity is None:
                    if user:
                        new_entity = Military.objects.get(cpf=user).entity 
                        row.entity = new_entity
                    else:
                        row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                row.save()
            except Exception as e:
                logger.error('Error while update entity tattoo - {}'.format(e))
                if row.entity is None:
                    row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                    row.save()
            finally:
                total_percents = (i / total * 100)
                progress_recorder.set_progress(i, total, f'Concluído {total_percents}%')
    else: 
        progress_recorder.set_progress(0, 0, f'Concluído 100%')

@shared_task(bind=True)
def task_set_entity_physical(self):
    rows = Physical.objects.all()
    if rows:
        i = 0
        total = int(rows.count())
        print(total)
        progress_recorder = ProgressRecorder(self)
        for row in rows:
            i += 1
            try:
                user = row.created_by
                entity = row.entity
                if entity is None:
                    if user:
                        new_entity = Military.objects.get(cpf=user).entity 
                        row.entity = new_entity
                    else:
                        row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                row.save()
            except Exception as e:
                logger.error('Error while update entity physical - {}'.format(e))
                if row.entity is None:
                    row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                    row.save()
            finally:
                total_percents = (i / total * 100)
                progress_recorder.set_progress(i, total, f'Concluído {total_percents}%')
    else: 
        progress_recorder.set_progress(0, 0, f'Concluído 100%')

@shared_task(bind=True)
def task_set_entity_face(self):
    rows = Face.objects.all()
    if rows:
        i = 0
        total = int(rows.count())
        print(total)
        progress_recorder = ProgressRecorder(self)
        for row in rows:
            i += 1
            try:
                user = row.created_by
                entity = row.entity
                if entity is None:
                    if user:
                        new_entity = Military.objects.get(cpf=user).entity 
                        row.entity = new_entity
                    else:
                        row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                row.save()
            except Exception as e:
                logger.error('Error while update entity face - {}'.format(e))
                if row.entity is None:
                    row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                    row.save()
            finally:
                total_percents = (i / total * 100)
                progress_recorder.set_progress(i, total, f'Concluído {total_percents}%')
    else: 
        progress_recorder.set_progress(0, 0, f'Concluído 100%')