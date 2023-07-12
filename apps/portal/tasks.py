from datetime import datetime as date

from django.core.exceptions import ObjectDoesNotExist
from django.core import files
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import logging

from .models import Entity, Military, HistoryTransfer, Promotion
from .helpers import getMilitaryImageFile
from .services import get_data_entity_api_portal, get_data_military_api_portal

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def task_get_entity_from_portal(self):
    data = get_data_entity_api_portal(0)
    progress_recorder = ProgressRecorder(self)
    if data:
        # Gets an extra page to receive data left over from division by 10
        quantidade_paginas = int(data['count'] / 10) + 2
        if quantidade_paginas > 0:
            for i in range(1, quantidade_paginas):
                results = data['results']
                for result in results:
                    Entity.objects.update_or_create(id_portal=result['id'], name=result['name'], code=result['code'], father=result['father'],
                                                    child_exists=result['child_exists'], category=result['category'],
                                                    hierarchy=result['hierarchy'])

                data = get_data_entity_api_portal(i * 10)
                total_percents = ((i / 10) * 100)
                progress_recorder.set_progress(
                    i + 1, 10, f'Concluído {total_percents}%')
    else:
        progress_recorder.set_progress(0, 0, f'Concluído 100%')


@shared_task(bind=True)
def task_get_military_from_portal(self):
    datas = get_data_military_api_portal(0)
    progress_recorder = ProgressRecorder(self)
    if datas:
        quantidade_paginas = int(datas['count'] / 10) + 2

        if quantidade_paginas > 0:
            for i in range(1, quantidade_paginas):
                results = datas['results']

                for result in results:
                    unit = Entity.objects.get(code=result['unit'])
                    militaryInSai = Military.objects.filter(
                        register=result['register'])
                    if militaryInSai.exists():
                        print('Unidade anterir')
                        print(militaryInSai)
                        print('__________________')
                        military = Military.objects.filter(
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
                            if result['image']:
                                military.url_image = result['image']
                            else:
                                military.url_image = 'https://imgur.com/jS8iL9p'
                            military.save()

                            # Saving image from military
                            image_file = getMilitaryImageFile(result['image'])
                            if image_file:
                                military.image.save("{}.jpg".format(
                                    military.cpf), files.File(open(image_file[0], 'rb')))

                        MilitaryHistoryTransfer = HistoryTransfer.objects.filter(
                            military__register=result['register'])
                        print('Unidade nova')
                        print(military)

                        if not (MilitaryHistoryTransfer.filter(
                                entity__code=result['unit'])):

                            HistoryTransfer.objects.filter(
                                military__register=result['register'], date_finish__isnull=True).update(
                                date_finish=date.now(),
                                obs="Militar saiu da unidade")

                            unit = Entity.objects.get(code=result['unit'])
                            mili = Military.objects.get(
                                register=result['register'])
                            HistoryTransfer.objects.create(
                                military=mili, entity=unit, date_start=date.now(), obs="Militar mudou de unidade")

                        MilitaryPromotion = Promotion.objects.filter(
                            military__register=result['register'])

                        if not (MilitaryPromotion.filter(
                                rank=result['rank'])):
                            mili = Military.objects.get(
                                register=result['register'])
                            Promotion.objects.create(
                                military=mili, rank=result['rank'])

                    else:

                        # unit = Entity.objects.get(code=result['unit'])
                        military = Military.objects.create(
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
                            url_image=result['image'])

                        # Saving image from military
                        image_file = getMilitaryImageFile(result['image'])
                        military.image.save("{}.jpg".format(
                            military.cpf), files.File(open(image_file[0], 'rb')))

                        HistoryTransfer.objects.create(
                            military=military, entity=unit, date_start=date.now(), obs="Primeiro cadastro")

                        Promotion.objects.create(
                            military=military, rank=result['rank'])

                datas = get_data_military_api_portal(i * 10)
                total_percents = ((i / 10) * 100)
                progress_recorder.set_progress(
                    i + 1, 10, f'Concluído {total_percents}%')

    else:
        progress_recorder.set_progress(0, 0, f'Concluído 100%')
