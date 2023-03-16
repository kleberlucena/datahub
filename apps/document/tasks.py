from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from celery_progress.backend import ProgressRecorder
import logging

from .models import Document, DocumentImage
from apps.portal.models import Military, Entity 

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task(bind=True)
def task_set_entity_document(self):
    rows = Document.objects.all()
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
                logger.error('Error while update entity document - {}'.format(e))
                if row.entity is None:
                    row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                    row.save()
            finally:
                total_percents = (i / total * 100)
                progress_recorder.set_progress(i, total, f'Concluído {total_percents}%')
    else: 
        progress_recorder.set_progress(0, 0, f'Concluído 100%')

@shared_task(bind=True)
def task_set_entity_document_image(self):
    rows = DocumentImage.objects.all()
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
                logger.error('Error while update entity document image - {}'.format(e))
                if row.entity is None:
                    row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
                    row.save()
            finally:
                total_percents = (i / total * 100)
                progress_recorder.set_progress(i, total, f'Concluído {total_percents}%')
    else: 
        progress_recorder.set_progress(0, 0, f'Concluído 100%')