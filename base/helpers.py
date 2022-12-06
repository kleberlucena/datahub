import requests
import json
from django.conf import settings
from numpy import base_repr


def get_watermark_url(old_url, user_number):
    num = base_repr(int(user_number), 36)
    body = { 
        "waterMarkId": num, 
        "imagePath": old_url,
    }
    headers = {
        "Authorization": settings.WATERMARK_SECRET,
        "Content-Type": "application/json",
    }
    response = requests.post(f"{settings.WATERMARK_HOST}/get-signed-url", 
        json = body,
        headers = headers,
    )
    return json.loads(response.text)['signedUrl']
