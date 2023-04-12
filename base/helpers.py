import re
import urllib.parse
import base64
import calendar
from hashlib import sha1
from hmac import new as hmac
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from numpy import base_repr


INVALIDS_CPFS = ("11111111111", "22222222222", "33333333333", "44444444444", "55555555555",
                 "66666666666", "77777777777", "88888888888", "99999999999", "00000000000")


def digit_generator(cpf, weight):
    sum_digit = 0
    for n in range(weight - 1):
        sum_digit = sum_digit + int(cpf[n]) * weight
        weight = weight - 1

    digit = 11 - sum_digit % 11
    return 0 if digit > 9 else digit


def validate_cpf(value):
    # Extract numbers from string
    cpf = re.sub("[^0-9]", "", value)
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 números', 'invalid')

    # Calculate first validator digit from string
    first_digit = digit_generator(cpf, weight=10)

    # Calculate second validator digit from string
    second_digit = digit_generator(cpf, weight=11)

    # Checks whether the cpf is on the list of invalid persons or if a check digit does not match the digits calculated
    # in the expression
    if cpf in INVALIDS_CPFS or (not cpf[-2:] == f'{first_digit}{second_digit}'):
        raise ValidationError('Número de CPF inválido', 'invalid')
    return cpf

"""
Função para gerar uma string check para servir como
validação na hora de baixar a imagem através do link fornecido
pela URL assinada do imgproxy.
"""
def get_verified_check(sum):
    return hmac(bytes(settings.WATERMARK_SECRET, "utf-8"), sum.encode("utf-8"), sha1).hexdigest() 


"""
Função para obter a URL assinada da imagem com a marca dágua.
Essa URL assinada NÃO faz requisição para o imgproxy.
"""
def get_watermark_url(old_url, user_number):

    if settings.DEBUG == True or not hasattr(settings, 'WATERMARK_ACTIVE') or settings.WATERMARK_ACTIVE == 'on':
        return old_url
    else:
        """"
        A variável num pega o CPF do usuário e converte para base36.
        Essa conversão está sendo feita enquanto não definimos qual será a string
        que irá identificar a marca dágua do usuário.
        """
        num = re.sub(r"[^0-9]", "", user_number)
        key = base_repr(int(num), 36)
        exp = calendar.timegm((datetime.now() + timedelta(minutes = 10)).timetuple())
        encoded_img_path = urllib.parse.quote_plus(old_url)
        img_path_64 = base64.b64encode(bytes(encoded_img_path, 'utf-8')).decode("utf-8")
        check = get_verified_check(str(key) + str(exp) + img_path_64)
        signed_url = "{}/image?check={}&key={}&exp={}&imagePath={}".format(settings.WATERMARK_HOST, check, key, exp, img_path_64)
        return signed_url


def get_image_variation(self, object, variation):
        request = self.context.get('request', None)
        if request:
            img_name = object.file.name
            parts = img_name.split('.')
            img_variation_name = str(parts[0]) + '.' + variation + '.' + str(parts[1])
            url = object.file.storage.url(img_variation_name)
            return get_watermark_url(url, request.user.username)