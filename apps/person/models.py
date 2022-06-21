import uuid
from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class Person(Base):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return f"{self.uuid}"
    
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    

class PersonDocument(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='person_documents', related_query_name='person_document', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.uuid}"
    
    class Meta:
        verbose_name = "Documento de Pessoa"
        verbose_name_plural = "Documentos de Pessoas"
    

class PersonNickname(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='person_nicknames', related_query_name='person_nickname', on_delete=models.CASCADE)
    nickname = models.CharField("Alcunha", max_length=255)
    
    def __str__(self):
        return f"{self.nickname}"

    class Meta:
        verbose_name = "Alcunha de Pessoa"
        verbose_name_plural = "Alcunhas de Pessoas"
        
        