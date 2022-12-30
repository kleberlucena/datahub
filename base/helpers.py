import requests
import json
from django.conf import settings
from numpy import base_repr


def get_watermark_url(old_url, user_number):

    if settings.DEBUG:
        return old_url

    num = base_repr(int(user_number), 36)
    body = { 
        "enjoyer": num,
        "image_path": old_url,
    }
    headers = {
        "Authorization": 'Token {}'.format(settings.SERVICES_SECRET),
        "Content-Type": "application/json",
    }
    response = requests.post(f"{settings.SERVICES_HOST}/api/v1/mark/get-signed-url/",
        json = body,
        headers = headers,
    )

    return json.loads(response.text)['signed_url_marked']
