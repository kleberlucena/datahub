import requests
import json
from django.conf import settings
from numpy import base_repr


def get_watermark_url(old_url, user_number):

    if settings.DEBUG:
        return old_url
    elif settings.WATERMARK_FLUX == 'IMGPROXY':
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
    else:
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



def get_image_variation(self, object, variation):
        request = self.context.get('request', None)
        if request:
            img_name = object.file.name
            parts = img_name.split('.')
            img_thumb_name = str(parts[0]) + '.' + variation + '.' + str(parts[1])
            print(img_thumb_name)            
            url = object.file.storage.url(img_thumb_name)
            return get_watermark_url(url, request.user.username)