from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import requests
import logging
import json
import uuid
import io
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from django.conf import settings

from . import models
from . import tasks

logger = logging.getLogger(__name__)

# Config watermark position
small_height = 20
medium_height = 40
large_height = 50
color_fill = (93, 173, 226, 75)
color_fill_shadow = (39, 174, 96, 125)

TEMPLATES_MARKS = {
    "small": [(7, 5 + small_height * i) for i in range(6)] +
             [(67, 5 + small_height * i) for i in range(6)],

    "medium": [(15, 10 + medium_height * i) for i in range(15)] +
              [(106, 10 + medium_height * i) for i in range(15)] +
              [(202, 10 + medium_height * i) for i in range(15)] +
              [(298, 10 + medium_height * i) for i in range(15)] +
              [(394, 10 + medium_height * i) for i in range(15)],

    "large": [(25, 15 + large_height * i) for i in range(15)] +
             [(140, 15 + large_height * i) for i in range(15)] +
             [(255, 15 + large_height * i) for i in range(15)] +
             [(370, 15 + large_height * i) for i in range(15)] +
             [(485, 15 + large_height * i) for i in range(15)] +
             [(600, 15 + large_height * i) for i in range(15)],
}


# Watermark
def handle(image_url, user_id):
    url_temporary = create_temporary_url(user_id)
    tasks.process_watermark(user_id, url_temporary.pk, image_url)
    return url_temporary.temporary_url
    
    
def calculate_positions_mark_custom(img_width, img_height):
    """
    It receives the dimensions of the images to be worked on.
    Returns a list of tuples with positions (x, y) where watermarks should be saved.
    """
    horizontal_quantity = int((img_width - 25) / 115)
    horizontal_rest = int((img_width - 25) % 115)
    horizontal_adjust = int(horizontal_rest / (horizontal_quantity + 1))
    vertical_quantity = int((img_height - 15) / 49)
    vertical_rest = int((img_height - 15) % 49)
    vertical_adjust = int(vertical_rest / (vertical_quantity + 1))

    watermark_positions = []

    for indice_horizontal in range(horizontal_quantity):
        x = 25 + horizontal_adjust + (indice_horizontal * 115) + (indice_horizontal * horizontal_adjust)
        for indice_vertical in range(vertical_quantity):
            y = 15 + vertical_adjust + (indice_vertical * large_height) + (indice_vertical * vertical_adjust)
            watermark_positions.append((x, y))

    return watermark_positions


def calculate_font_size(img_width):
    """Get the width of the image and returns the font size of the watermark"""
    if img_width == 128:
        font_size = 15
    elif img_width == 480:
        font_size = 20
    else:
        font_size = 25
    return font_size


def create_watermark_template_user(mark_text, img_width, img_height):
    font_size = calculate_font_size(img_width)
    font_path = finders.find('sti/fonts/Poppins-Regular.ttf')
    font = ImageFont.truetype(font_path, font_size)

    watermark_layer = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    if img_width == 128:
        template_number = "small"
        name_image = "{}_small.png".format(mark_text)
    elif img_width == 480:
        template_number = "medium"
        name_image = "{}_medium.png".format(mark_text)
    elif img_width == 720:
        template_number = "large"
        name_image = "{}_large.png".format(mark_text)
    else:
        template_number = None
        name_image = "{}_whithout_template.png".format(mark_text)

    if template_number:
        mark_positions = TEMPLATES_MARKS[template_number]
    else:
        mark_positions = calculate_positions_mark_custom(img_width, img_height)
        
    for mark_position in mark_positions:
        draw.text(mark_position, mark_text, font=font, fill=color_fill_shadow)
        draw.text((mark_position[0] + 1, mark_position[1] + 1), mark_text, font=font, fill=color_fill)
        
    image_file = io.BytesIO()
    watermark_layer.save(image_file, 'PNG')
    image_file.seek(0)
    return (name_image, image_file)


def add_watermark_image(image_url, mark):
    urllib.request.urlretrieve(image_url, 'file_name')
    img = Image.open('file_name')
    img_width, img_height = img.size
    
    if img_width == 128:
        watermark_layer = models.MarkTemplates.objects.get(uuid_user_mark=mark.uuid).mark_128
    elif img_width == 480:
        watermark_layer = models.MarkTemplates.objects.get(uuid_user_mark=mark.uuid).mark_480
    elif img_width == 720:
        watermark_layer = models.MarkTemplates.objects.get(uuid_user_mark=mark.uuid).mark_720
    else:
        watermark_layer = create_watermark_template_user(mark.mark_text, img_width, img_height)[1]

    image_watermark = Image.open(watermark_layer)

    # Sobreponha a camada transparente com marca d'água na imagem original
    img = Image.alpha_composite(img.convert('RGBA'), image_watermark)
    return img


# Url temporary
def get_url_momentum(uuid):
    '''
    Verifica se a imagem já está disponível e retorna ela ou None caso não esteja processada ainda.
    '''
    try:
        url_received = models.TemporaryURL.objects.get(uuid=uuid)
        url_finally = url_received.photo.url
        data = {'url': url_finally}
    except:
        data = None
    finally:
        return data


def create_temporary_url(user_id):
    '''Cria url temporária para a imagem a ser processada'''
    uuid_generated = uuid.uuid4()
    url_temp = "{}/api/v1/watermark/{}/{}/".format(settings.SELF_URL_BASE, user_id, uuid_generated)
    time_expiration = datetime.now() + timedelta(minutes=10)
    new_temporary_url = models.TemporaryURL.objects.create(uuid=uuid_generated, temporary_url=url_temp,
                                                           expiration_date=time_expiration)
    return new_temporary_url


# Mark
def get_mark_services(enjoyer):
    ''' Get mark text from system Services '''
    services_url = f"{settings.SERVICES_URL}{settings.SERVICES_ENDPOINT_MARK}{enjoyer}"
    content_type = 'application/json'
    authorization = f"Token {settings.SERVICES_TOKEN}"
    headers = {
        'Content-Type': content_type,
        'Authorization': authorization,
    }

    try:
        response = requests.get(services_url, headers=headers, timeout=(15, 180))
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            logger.warning(f'RequestI inválida: {response.status_code}')
    except Exception as e:
        raise logger.error('Error while get by razao - {}'.format(e))


def get_mark_user(user_id):
    ''' Get text mark from user request'''
    try:
        mark_user = models.UserMark.objects.get(user__pk=user_id, active=True)
        if mark_user:
            return mark_user
    except Exception as e:
        enjoyer = User.objects.get(id=user_id).username
        try:
            response = get_mark_services(enjoyer)
            mark_text = response['mark']          
            user = User.objects.get(id=user_id)
            return models.UserMark.objects.create(mark_text=mark_text, user=user)
        except Exception as e:
            if models.UserMark.objects.all().count() > 0:
                last_mark = models.UserMark.objects.latest('created_at')
                mark_int = int(last_mark.mark_text[-5:]) + 1
                new_mark_text = str(mark_int).zfill(5)
                new_mark = "B" + new_mark_text
            else:
                new_mark = "B00000"
            
            return models.UserMark.objects.create(mark_text=new_mark, user=User.objects.get(id=user_id))
                
            
            
            
