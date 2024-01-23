import uuid
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from apps.address.models import Address
from apps.portal.models import Enjoyer, Entity


class Category(models.Model):
    name = models.CharField("Nome", max_length=50, unique=True)
    description = models.CharField("Descrição", max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Area(models.Model):
    name = models.CharField("Nome", max_length=50, unique=True)
    description = models.CharField("Descrição", max_length=300, null=True, blank=True)
    area_polygon = models.PolygonField("Área delimitada", null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

    
    # def get_centroid(self):
    #     # Verifica se o campo area_polygon está definido
    #     if self.area_polygon:
    #         # Calcula o centroide usando a biblioteca GEOSGeometry
    #         centroid = self.area_polygon.centroid
    #         return centroid
    #     else:
    #         return None  # Retorna None se não houver polígono definido
        


class SpotType(models.Model):
    name = models.CharField("Categoria",max_length=100, null=False, blank=False)
    spot_type_father = models.ForeignKey('self', null=True, blank=True, related_name='spot_type_son', on_delete=models.CASCADE, verbose_name='Categoria Pai')
    update_time = models.IntegerField(null=False, blank=False, default=30)

    def __str__(self):
        return self.name
    

class Spot(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField("Ponto", max_length=100, null=False, blank=False)
    details = models.CharField("Informações adicionais", max_length=300, null=True, blank=True)
    spot_type = models.ForeignKey(SpotType, on_delete=models.CASCADE, null=False, blank=False)
    latitude = models.FloatField("Latitude", default=0.0, null=False, blank=False)
    longitude = models.FloatField("Longitude", default=0.0, null=False, blank=False)
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='georef_spots_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='georef_spots_updated')
    update_score = models.IntegerField(null=True, blank=True)
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
        related_name=('georef_spots_addresses'),
    )
    origin_system = models.CharField("Sistema de origem", default="bacinf", max_length=100, null=False, blank=False)
    origin_app = models.CharField("App de origem", default="módulo de georeferenciamento", max_length=100, null=False, blank=False)
    user_name = models.ForeignKey(
        Enjoyer,
        related_name = 'georef_spots_username',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    user_unit = models.ForeignKey(
        Entity,
        related_name = 'georef_spots_entity',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        related_name='georef_spot_user',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    
class SpotAddresses(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='georef_spots_address')
    addressType = models.CharField(max_length=64, null=True, blank=True)


        


