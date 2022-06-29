import uuid
from django.db import models

from apps.address.models import Address
from apps.image.models import Image


class Base(models.Model):
    created = models.DateTimeField('Criado', auto_now_add=True)
    updated = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class Person(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return f"{self.uuid}"
    
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    

class PersonDocument(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='person_document', related_query_name='person_document', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.uuid}"
    
    class Meta:
        verbose_name = "Documento de Pessoa"
        verbose_name_plural = "Documentos de Pessoas"
    

class PersonNickname(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='person_nickname', related_query_name='person_nickname', on_delete=models.CASCADE)
    nickname = models.CharField("Alcunha", max_length=255)
    
    def __str__(self):
        return f"{self.nickname}"

    class Meta:
        verbose_name = "Alcunha de Pessoa"
        verbose_name_plural = "Alcunhas de Pessoas"
        
        
class PersonAddress(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='person_address', related_query_name='person_address', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, related_name='address_person_address', related_query_name='address_person_address', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.uuid}"
    
    class Meta:
        verbose_name = "Endereço de Pessoa"
        verbose_name_plural = "Endereços de Pessoas"
        

class PersonImage(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='person_image', related_query_name='person_image', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='image_person_image', related_query_name='image_person_image', on_delete=models.CASCADE)
    description = models.CharField("Descrição", max_length=255)
    
    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Imagem de Pessoa"
        verbose_name_plural = "Imagens de Pessoas"
        
    
class PersonImageFace(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='person_image_face', related_query_name='person_image_face', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='image_person_image_face', related_query_name='image_person_image_face', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Imagem de Face de Pessoa"
        verbose_name_plural = "Imagens de Face de Pessoas"
        