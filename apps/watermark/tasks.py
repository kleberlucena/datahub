from celery import shared_task
from io import BytesIO
from django.core.files import File
from django.utils import timezone
import logging

from . import helpers
from . import models

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_watermark(self, user_id, url_pk, image_url):
    # verify mark passando o user
    mark = helpers.get_mark_user(user_id)
    img = helpers.add_watermark_image(image_url, mark)
    img = img.convert("RGB")
    buf = BytesIO()
    img.save(buf, format='JPEG', quality=90)
    buf.seek(0)

    url = models.TemporaryURL.objects.get(pk=url_pk)
    url.photo.save("{}.jpg".format(url_pk), File(buf), save=True)
    

@shared_task(bind=True)
def deactivate_mark(self):
    user_mark_queryset = models.UserMark.objects.filter(active=True)()
    models.MarkTemplates.objects.filter(uuid_user_mark__in=[user_mark.uuid for user_mark in user_mark_queryset])
    user_mark_queryset.update(active=False)
    logger.info('Deactivate all UserMark successfully')
    

@shared_task(bind=True)
def remove_temporary_url(self):
    models.TemporaryURL.objects.filter(expiration_date__lte=timezone.now()).delete()
    logger.info('Delete all URLTemporary successfully')
