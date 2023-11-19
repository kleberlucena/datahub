from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend
from localflavor.br.models import BRStateField, BRCPFField, BRPostalCodeField

from django.utils import timezone


class Base(models.Model):
    created_at = models.DateField('Criado', auto_now_add=True)
    updated_at = models.DateField('Atualizado', auto_now=True)
    active = models.BooleanField('Ativo', default=False)

    class Meta:
        abstract = True
        

class Gender(Base):
    """
    Categorias dos grupos, por exemplo: Polícia Militar da Paraíba, Público Civil, Policiamento Ostensivo, Inteligência
    """
    uuid_portal = models.UUIDField('UUID no Portal', editable=False, unique=True)
    name = models.CharField("Nome da categoria", max_length=100)
    description = models.CharField("Descrição da categoria de entidades", max_length=256, null=True, blank=True)    

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
        
    def __str__(self):
        return self.name


class OrganizationalHierarchy(Base):
    """
    Hierarquia organizacional dos grupos, por exemplo: Estado Maior Estratégico, Comando Geral, Batalhão, Seção
    """
    uuid_portal = models.UUIDField('UUID no Portal', editable=False, unique=True)
    name = models.CharField("Nome do tipo de entidade", max_length=100, null=True, blank=True)
    description = models.CharField("Descrição do tipo", max_length=256, null=True, blank=True)  

    class Meta:
        verbose_name = 'Hierarquia Organizacional'
        verbose_name_plural = 'Hierarquias Organizacionais'
        ordering = ['name']

    def __str__(self):
        return self.name


class Entity(Base):
    """
    Entidades em geral. Ex: PMPB|QCG|EME|EM2|STI|
    """
    name = models.CharField("Nome da entidade", max_length=100)
    father = models.CharField('Código da Entidade pai no EM8', max_length=7, default=0)
    dad = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Entidade superior")
    child_exists = models.BooleanField("A entidade tem filhos?", default=False)
    uuid_portal = models.UUIDField('UUID no Portal', editable=True, blank=True, null=True)
    gender = models.ManyToManyField(Gender, blank=True, verbose_name="Categoria", related_name="entity")
    organization =  models.ForeignKey(OrganizationalHierarchy, null=True, blank=True, verbose_name="Hierarquia", default=None, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Entidade'
        verbose_name_plural = 'Entidades'
        ordering = ['name']

    def __str__(self):
        return self.name


class Enjoyer(Base):
    username = models.CharField("Nome de usuário", max_length=100, unique=True)
    first_name = models.CharField("Primeiro nome", max_length=100)
    last_name = models.CharField("Último nome", max_length=100)
    full_name = models.CharField("Nome Completo", max_length=200, blank=True, null=True)
    email = models.EmailField("Email", unique=True)
    birthdate = models.DateField("Data de nascimento", blank=True, null=True)
    phone = models.CharField("Número de telefone", max_length=36, blank=True, null=True)
    image = StdImageField(
        'Image', 
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='enjoyers',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, blank=True, null=True, delete_orphans=True
    )
    uuid_portal = models.UUIDField('UUID no Portal', editable=False, unique=True)
    
    entity = models.ForeignKey(Entity, related_name='entity_enjoyer', null=True, blank=True, on_delete=models.PROTECT)    
    user = models.OneToOneField(User, related_name='enjoyer', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Utilizador'
        verbose_name_plural = 'Utilizadores'

    def get_absolute_url(self):
        return reverse('enjoyer:enjoyer_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "{} - {} {}".format(self.username, self.first_name, self.last_name)


class Military(Base):
    GENRE = (
        ('M', 'Masculino'),
        ('F', 'Feminino')
    )
    rank = models.CharField("Patente", max_length=36,  blank=True, null=True)
    name = models.CharField("Nome completo", max_length=256,  blank=True, null=True)
    nickname = models.CharField("Nome de guerra", max_length=100,  blank=True, null=True)
    admission_date = models.DateField("Data de admissão", blank=True, null=True)
    birthdate = models.DateField("Data de nascimento", blank=True, null=True)
    register = models.CharField("Matricula", max_length=7,  blank=True, null=True)
    activity_status = models.CharField("Regime", max_length=100,  blank=True, null=True)
    cpf = BRCPFField("CPF", blank=True, null=True)
    genre = models.CharField("Gênero", max_length=1, blank=True, null=True, choices=GENRE)
    email = models.CharField("Email", max_length=256, blank=True, null=True)
    father = models.CharField("Pai", max_length=256, blank=True, null=True)
    mather = models.CharField("Mãe", max_length=256, blank=True, null=True)
    place_of_birth = models.CharField("Naturalidade", max_length=64, blank=True, null=True)
    marital_status = models.CharField("Estado Civil", max_length=64, blank=True, null=True)
    phone = models.CharField("Telefone", max_length=36, blank=True, null=True)
    address = models.CharField("Endereço", max_length=256, blank=True, null=True)
    number = models.CharField("Número", max_length=16, blank=True, null=True, default='S/N')
    complement = models.CharField("Complemento", max_length=100, blank=True, null=True)
    district = models.CharField("Bairro", max_length=100, blank=True, null=True)
    city = models.CharField("Cidade", max_length=100, blank=True, null=True)
    state = BRStateField("Estado", blank=True, null=True)
    zipcode = BRPostalCodeField("CEP", blank=True, null=True)
    office = models.CharField("Função", max_length=100, blank=True, null=True)
    military_identity = models.CharField("Identidade Militar", max_length=36, blank=True, null=True)
    cnh = models.CharField("Carteira de Motorista", max_length=36, blank=True, null=True)
    rg = models.CharField("Registro Geral", max_length=36, blank=True, null=True)
    orgao_expeditor_rg = models.CharField("Órgão Expeditor", max_length=16, blank=True, null=True)
    uuid_portal = models.UUIDField('UUID no Portal', editable=True, blank=True, null=True)
    image = StdImageField(
        'Image', 
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='militaries_pmpb',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, blank=True, null=True, delete_orphans=True
    )
    
    entity = models.ForeignKey(Entity, null=True, blank=True, related_name='military', on_delete=models.SET_NULL)
    user = models.OneToOneField(User, related_name='military', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        unique_together = ('register', 'cpf',)
        verbose_name = 'Policial Militar'
        verbose_name_plural = 'Policiais Militares'

    def __str__(self):
        return "{} {}".format(self.rank, self.nickname)


# class HistoryTransfer(Base):
#     entity = models.ForeignKey(Entity, verbose_name="Unidade",
#                                default=0, to_field='code', on_delete=models.CASCADE)
#     military = models.ForeignKey(Military, on_delete=models.CASCADE)
#     obs = models.CharField(max_length=255, blank=True, null=True)
#     date_start = models.DateField('Data início', default=timezone.now)
#     date_finish = models.DateField('Data fim', blank=True, null=True)

#     class Meta:
#         verbose_name = 'Transferência'
#         verbose_name_plural = 'Transferências'

#     def __str__(self):
#         return "{} {}".format(self.entity, self.military)


# class Promotion(Base):
#     rank = models.CharField("Patente", max_length=36, blank=False)
#     military = models.ForeignKey(Military, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Promoção'
#         verbose_name_plural = 'Promoções'

#     def __str__(self):
#         return "{}".format(self.rank)
