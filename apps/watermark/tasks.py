from celery import shared_task
from io import BytesIO
from django.core.files import File

from . import helpers
from . import models


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
