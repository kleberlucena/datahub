import uuid
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend
from django.contrib.gis.db import models
from apps.address.models import Address
from apps.portal import models as portal_models
from apps.portal.models import Entity, Military, Promotion, HistoryTransfer




class SpotType(models.Model):
    name = models.CharField("Categoria",max_length=100, null=False, blank=False)
    spot_type_father = models.ForeignKey('self', null=True, blank=True, related_name='spot_type_son', on_delete=models.CASCADE, verbose_name='Categoria Pai')
    update_time = models.IntegerField(null=False, blank=False, default=30)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Tag", max_length=50)
    details = models.CharField("Descrição", max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Qpp(models.Model):
    name = models.CharField("QPP", max_length=50)
    details = models.CharField("Descrição", max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name
    
# class Network(models.Model):
#     name = models.CharField("Nome da rede", max_length=200)
#     responsibles = models.ManyToManyField(Military, related_name='networks_responsible')
#     details = models.CharField("Informações adicionais", max_length=300, null=True, blank=True)
#     #unit = models.ForeignKey(Entity, related_name='respondible_unit', on_delete=models.RESTRICT)

#     def __str__(self):
#         return self.name

class Network(models.Model):
    name = models.CharField("Nome da rede", max_length=200)
    details = models.CharField("Informações adicionais", max_length=300, null=True, blank=True)
    responsibles = models.ManyToManyField(
        Promotion,
        through='NetworkResponsible',
        through_fields=('network', 'responsible'),
    )

    def __str__(self):
        return self.name

class NetworkResponsible(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    responsible = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    active = models.BooleanField(null=True, blank=True, default=True)

    class Meta:
        unique_together = ['network', 'responsible']

    def __str__(self):
        return "{} {}".format(self.responsible.rank, self.responsible.military)

        
    
class Image(models.Model): #### IMAGEM DO SPOT
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField("descrição", max_length=255, blank=True, null=True)
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='images_created')
    imageSpot = StdImageField(
        'Imagem', 
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='protect_network_img',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True
    )

    def __str__(self):
        return f"{self.imageSpot}"

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"


# class ContactImage(models.Model): #### IMAGEM DO CONTATO
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     contact = models.ForeignKey('ContactInfo', on_delete=models.CASCADE)
#     created_at = models.DateTimeField('Criado', auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='contact_images_created')
#     imageContact = StdImageField(
#         'Imagem', 
#         storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
#         upload_to='protect_network_img',
#         variations={
#             'large': {'width': 720, 'height': 720, 'crop': True},
#             'medium': {'width': 480, 'height': 480, 'crop': True},
#             'thumbnail': {'width': 128, 'height': 128, 'crop': True},
#         }, delete_orphans=True
#     )

#     def __str__(self):
#         return f"{self.imageContact}"

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"        


class Spot(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField("Ponto", max_length=100, null=False, blank=False)
    details = models.CharField("Informações adicionais", max_length=300, null=True, blank=True)
    spot_type = models.ForeignKey(SpotType, on_delete=models.CASCADE, null=False, blank=False)
    latitude = models.FloatField("Latitude", default=0.0, null=False, blank=False)
    longitude = models.FloatField("Longitude", default=0.0, null=False, blank=False)
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='spots_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='spots_updated')
    tags = models.ManyToManyField(Tag, blank=True)
    update_score = models.IntegerField(null=True, blank=True)
    user_unit = models.ForeignKey(portal_models.Promotion, on_delete=models.PROTECT,verbose_name="Militar", related_name='spots')
    next_update = models.IntegerField(null=True, blank=True)
    is_temporary = models.BooleanField(null=True, blank=True, default=False)
    date_initial = models.DateTimeField(null=True, blank=True)
    date_final = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(null=True, blank=True, default=True)
    location = models.PointField("Localização", srid=4326, null=True, blank=True)
    addresses = models.ManyToManyField(
        Address,
        through='SpotAddresses',
        through_fields=('spot', 'address'),
    )
    is_headquarters = models.BooleanField(default=True, null=False, blank=False)
    cnpj = models.CharField(max_length=20, null=True, blank=True)
    parent_company = models.CharField(max_length=20, null=True, blank=True)
    spot_network = models.ForeignKey(Network, on_delete=models.CASCADE, null=True, blank=False)
    QPP = models.ForeignKey(Qpp, on_delete=models.CASCADE, null=False, blank=False)
    
       
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class SpotAddresses(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    addressType = models.CharField(max_length=64, null=True, blank=True)
    

class ContactInfo(models.Model):
    name = models.CharField("Contato", max_length=200, default="", null=False, blank=False)
    phone = models.CharField("Telefone de contato", max_length=200, default="", null=True, blank=True)
    role = models.CharField("Título ou função", max_length=200, default="", null=True, blank=True)
    email = models.CharField("E-mail", max_length=200, default="", null=True, blank=True)
    rg = models.CharField("RG", max_length=20, default="", null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, default="", null=True, blank=True)
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE)

    
class OpeningHours(models.Model):
    OPENED_OPTIONS = [
        (True, 'Sim'),
        (False, 'Não'),
    ]
    opened_mon = models.BooleanField(choices=OPENED_OPTIONS, blank=True, null=True, default=True)
    open_time_mon = models.TimeField(blank=True, null=True)
    close_time_mon = models.TimeField(blank=True, null=True)
    opened_tue = models.BooleanField(choices=OPENED_OPTIONS, blank=True, null=True, default=True)
    open_time_tue = models.TimeField(blank=True, null=True)
    close_time_tue = models.TimeField(blank=True, null=True)
    opened_wed = models.BooleanField(choices=OPENED_OPTIONS, blank=True, null=True, default=True)
    open_time_wed = models.TimeField(blank=True, null=True)
    close_time_wed = models.TimeField(blank=True, null=True)
    opened_thu = models.BooleanField(choices=OPENED_OPTIONS, blank=True, null=True, default=True)
    open_time_thu = models.TimeField(blank=True, null=True)
    close_time_thu = models.TimeField(blank=True, null=True)
    opened_fri = models.BooleanField(choices=OPENED_OPTIONS, blank=True, null=True, default=True)
    open_time_fri = models.TimeField(blank=True, null=True)
    close_time_fri = models.TimeField(blank=True, null=True)
    opened_sat = models.BooleanField(choices=OPENED_OPTIONS, blank=True, null=True, default=True)
    open_time_sat = models.TimeField(blank=True, null=True)
    close_time_sat = models.TimeField(blank=True, null=True)
    opened_sun = models.BooleanField(choices=OPENED_OPTIONS, blank=True, null=True, default=True)
    open_time_sun = models.TimeField(blank=True, null=True)
    close_time_sun = models.TimeField(blank=True, null=True)
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE, related_name='opening_hours')

    def __str__(self):
        return self.spot
    


class SecuritySurvey(models.Model):
    spot = models.ForeignKey('Spot', on_delete=models.CASCADE, related_name='security_survey')
    security_cameras = models.BooleanField(blank=False, null=False)
    security_cameras_rec = models.BooleanField(blank=False, null=False)
    private_security = models.BooleanField(blank=False, null=False)
    external_lights = models.BooleanField(blank=False, null=False)
    alarm_system = models.BooleanField(blank=False, null=False)
    fire_extinguisher = models.BooleanField(blank=False, null=False)
    emergency_out = models.BooleanField(blank=False, null=False)
    fire_alarm_system = models.BooleanField(blank=False, null=False)
    security_barriers = models.BooleanField(blank=False, null=False)
    other_security_measures = models.TextField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.spot
