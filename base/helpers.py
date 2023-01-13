import requests
import json
from django.conf import settings
from numpy import base_repr


def get_watermark_url(old_url, user_number):

    if settings.DEBUG:
        return old_url
    else:
        num = base_repr(int(user_number), 36)
        body = { 
            "waterMarkId": num,
            "imagePath": old_url,
        }
        headers = {
            "Authorization": '9F4FE54F2555AD0AAA09E213977DAEE31A5DBAEBBB498822ECDCE5FBFF11F28B',
            "Content-Type": "application/json",
        }
        response = requests.post("http://10.0.1.57:9005/get-signed-url",
            json = body,
            headers = headers,
        )
        return json.loads(response.text)['signedUrl']
        



def get_image_variation(self, object, variation):
        request = self.context.get('request', None)
        if request:
            img_name = object.file.name
            parts = img_name.split('.')
            img_thumb_name = str(parts[0]) + '.' + variation + '.' + str(parts[1])
            print(img_thumb_name)            
            url = object.file.storage.url(img_thumb_name)
            return get_watermark_url(url, request.user.username)