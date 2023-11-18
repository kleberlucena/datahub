from datetime import datetime as date

from django.core.exceptions import ObjectDoesNotExist
from django.core import files
from django.contrib.auth.models import User
from django.db import IntegrityError
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import logging

# from .models import Entity, Military, HistoryTransfer, Promotion
# from .helpers import getMilitaryImageFile
# from .services import get_data_entity_api_portal, get_data_military_api_portal
from . import models, helpers, services

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def task_get_entity_from_portal(self):
    data = services.get_data_entity_api_portal(0)
    progress_recorder = ProgressRecorder(self)
    if data:
        # Gets an extra page to receive data left over from division by 10
        quantidade_paginas = int(data['count'] / 10) + 2
        if quantidade_paginas > 0:
            for i in range(1, quantidade_paginas):
                results = data['results']
                for result in results:
                    try:
                        entity = models.Entity.objects.get(id_portal=result['id'])
                        entity.name = result['name']
                        entity.code = result['code']
                        entity.father = result['father']
                        entity.child_exists = result['child_exists']
                        entity.category = result['category']
                        entity.hierarchy = result['hierarchy']
                        entity.save()
                    except models.Entity.DoesNotExist:
                        logger.info('Unidade nova vinda do portal - {}'.format(result['id']))
                        models.Entity.objects.create(id_portal=result['id'], name=result['name'], code=result['code'], father=result['father'],
                                                        child_exists=result['child_exists'], category=result['category'],
                                                        hierarchy=result['hierarchy'])
                    except IntegrityError as ie:
                        logger.error('Unidade com erro de integridade - {}'.format(ie))
                        models.Entity.objects.filter(id_portal=result['id']).update(name=result['name'], code=result['code'], father=result['father'],
                                                                                     child_exists=result[
                                                                                         'child_exists'], category=result['category'],
                                                                                     hierarchy=result['hierarchy'])
                    except Exception as e:
                        logger.error("Error, {}".format(e))
                data = services.get_data_entity_api_portal(i * 10)
                total_percents = ((i / 10) * 100)
                progress_recorder.set_progress(
                    i + 1, 10, f'Concluído {total_percents}%')
    else:
        progress_recorder.set_progress(0, 0, f'Concluído 100%')


@shared_task(bind=True)
def task_get_military_from_portal(self):
    datas = services.get_data_military_api_portal(0)
    progress_recorder = ProgressRecorder(self)
    if datas:
        quantidade_paginas = int(datas['count'] / 10) + 2

        if quantidade_paginas > 0:
            for i in range(1, quantidade_paginas):
                results = datas['results']

                for result in results:
                    unit = None
                    url_image = None
                    try:
                        unit = models.Entity.objects.get(code=result['unit'])
                    except Exception as e:
                        unit = None
                    if result['image']:
                        url_image = result['image']
                    else:
                        url_image = 'https://imgur.com/jS8iL9p'
                        
                    militaryInBacinf = models.Military.objects.filter(
                        register=result['register'])
                    if militaryInBacinf.exists():
                        military = models.Military.objects.filter(
                            register=result['register']).first()

                        if military:
                            military.entity = unit
                            military.name = result['name']
                            military.admission_date = result['admission_date']
                            military.birthdate = result['birthdate']
                            military.mather = result['mather']
                            military.place_of_birth = result['place_of_birth']
                            military.nickname = result['nickname']
                            military.activity_status = result['activity_status']
                            military.genre = result['genre']
                            military.email = result['email']
                            military.marital_status = result['marital_status']
                            military.phone = result['phone']
                            military.address = result['address']
                            military.number = result['number']
                            military.complement = result['complement']
                            military.district = result['district']
                            military.city = result['city']
                            military.state = result['state']
                            military.zipcode = result['zipcode']
                            military.register = result['register']
                            military.cpf = result['cpf']
                            military.url_image = url_image
                            military.save()

                            # Saving user from military
                            user = User.objects.filter(
                                username=military.cpf).first()
                            if user:
                                military.user = user

                            # Saving image from military
                            image_file = helpers.getMilitaryImageFile(result['image'])
                            if image_file:
                                military.image.save("{}.jpg".format(
                                    military.cpf), files.File(open(image_file[0], 'rb')))

                        MilitaryHistoryTransfer = models.HistoryTransfer.objects.filter(
                            military__register=result['register'])


                        if not (MilitaryHistoryTransfer.filter(
                                entity__code=result['unit'])):

                            models.HistoryTransfer.objects.filter(
                                military__register=result['register'], date_finish__isnull=True).update(
                                date_finish=date.now(),
                                obs="Militar saiu da unidade")
                            try:
                                unit = models.Entity.objects.get(code=result['unit'])
                                mili = models.Military.objects.get(
                                    register=result['register'])
                                models.HistoryTransfer.objects.create(
                                    military=mili, entity=unit, date_start=date.now(), obs="Militar mudou de unidade")
                            except models.Entity.DoesNotExist:
                                logger.error('Unidade não encotrada - {}'.format(result['unit']))
                            except models.Military.DoesNotExist:
                                logger.error('Militar não encontrado - {}'.format(result['register']))

                        MilitaryPromotion = models.Promotion.objects.filter(
                            military__register=result['register'])

                        if not (MilitaryPromotion.filter(
                                rank=result['rank'])):
                            mili = models.Military.objects.get(
                                register=result['register'])
                            models.Promotion.objects.create(
                                military=mili, rank=result['rank'])

                    else:

                        # unit = Entity.objects.get(code=result['unit'])
                        military = models.Military.objects.create(
                            entity=unit,
                            name=result['name'],
                            admission_date=result['admission_date'],
                            birthdate=result['birthdate'],
                            mather=result['mather'],
                            place_of_birth=result['place_of_birth'],
                            nickname=result['nickname'],
                            activity_status=result['activity_status'],
                            genre=result['genre'],
                            email=result['email'],
                            marital_status=result['marital_status'],
                            phone=result['phone'],
                            address=result['address'],
                            number=result['number'],
                            complement=result['complement'],
                            district=result['district'],
                            city=result['city'],
                            state=result['state'],
                            zipcode=result['zipcode'],
                            register=result['register'],
                            cpf=result['cpf'],
                            url_image=url_image)

                        # Saving user from military
                        user = User.objects.filter(
                            username=military.cpf).first()
                        if user:
                            military.user = user

                        # Saving image from military
                        try:
                            if url_image is not None:
                                image_file = helpers.getMilitaryImageFile(url_image)
                                military.image.save("{}.jpg".format(
                                military.cpf), files.File(open(image_file[0], 'rb')))
                        except Exception as e:
                            logger.error('Erro de inesperado ao salvar imagem - {}'.format(e))

                        models.HistoryTransfer.objects.create(
                            military=military, entity=unit, date_start=date.now(), obs="Primeiro cadastro")

                        models.Promotion.objects.create(
                            military=military, rank=result['rank'])

                datas = services.get_data_military_api_portal(i * 10)
                total_percents = ((i / 10) * 100)
                progress_recorder.set_progress(
                    i + 1, 10, f'Concluído {total_percents}%')

    else:
        progress_recorder.set_progress(0, 0, f'Concluído 100%')


@shared_task(bind=True)
def link_military(self, username):
    """
    Relaciona o militar a um usuário através de seu username
    """
    
    militaries = models.Military.objects.filter(cpf=username, user__isnull=True)
    
    for military in militaries:
        user = User.objects.get(username=username)
        military.user = user
        military.save()
        logger.info('Military linked successful with User Django behind username: {}'.format(username))
 