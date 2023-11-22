import uuid
import string
import random
from stdimage.models import StdImageField

from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models
from django_minio_backend import MinioBackend
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.portal.models import Military


class Base(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True

def validate_tamanho_arquivo(arquivo):
    tamanho_max = 10 * 1024 * 1024  # 10 MB em bytes
    if arquivo.size > tamanho_max:
        raise ValidationError('O tamanho máximo do arquivo é de 10 MB.')


class Entities(Base):
    entity = models.CharField(max_length=100)

    def __str__(self):
        return self.entity


class FlightNature(Base):
    nature = models.CharField(max_length=300)

    def __str__(self):
        return self.nature


class TypesOfOperations(Base):
    type_operation = models.CharField(max_length=100)

    def __str__(self):
        return self.type_operation


class CitiesPB(Base):
    cities_pb = models.CharField(max_length=100)

    def __str__(self):
        return self.cities_pb


class PoliceGroup(models.Model):
    driver = models.ForeignKey(Military, on_delete=models.SET_NULL, related_name='gu_driver', null=True)
    remote_pilot = models.ForeignKey(Military, on_delete=models.SET_NULL, related_name='gu_remote_pilot', null=True)
    observer_pilot = models.ForeignKey(Military, on_delete=models.SET_NULL, related_name='gu_observer_pilot', blank=True, null=True)
    phone = models.CharField(max_length=20, null=False, blank=False)
    location = models.ForeignKey(CitiesPB, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.remote_pilot} | {self.date} | {self.location}'
    
    
class Aircraft(Base):
    prefix = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    location = models.ForeignKey(CitiesPB, on_delete=models.SET_NULL, null=True)
    in_use = models.BooleanField(default=False, null=True, blank=True)
    aircraft_image = StdImageField(
        'Imagem',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True, null=True
    )
    
    def __str__(self):
        return "{} - {} - {}".format(self.prefix, self.model, self.brand)


def generate_hex_code():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(25))

class AicraftHistoric(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    aircraft_title = models.CharField(max_length=45, null=True)
    date = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=25, unique=True, default=generate_hex_code)
    num_propellers = models.IntegerField(default=4, null=False)
    num_batteries = models.IntegerField(default=4, null=False)
    batteries_loaded = models.BooleanField(default=True)
    control_battery_loaded = models.BooleanField(default=True)
    body = models.BooleanField(default=True)
    engine_rods = models.BooleanField(default=True)
    propellers = models.BooleanField(default=True)
    gimbal = models.BooleanField(default=True)
    spotlight = models.BooleanField(default=True)
    load_speaker = models.BooleanField(default=True)
    stroboscopic_light = models.BooleanField(default=True)
    cables = models.BooleanField(default=True)
    charger = models.BooleanField(default=True)
    smart_controller = models.BooleanField(default=True)
    controller = models.BooleanField(default=True)
    sd_card = models.BooleanField(default=True)
    imu = models.BooleanField(default=True)
    compass = models.BooleanField(default=True)
    signal_transmission = models.BooleanField(default=True)
    system_rtk_ppk = models.BooleanField(default=True)
    video_signal = models.BooleanField(default=True)
    telemetry = models.BooleanField(default=True)
    parachute = models.BooleanField(default=True)
    changes = models.TextField()

    def __str__(self):
        return f"Histórico de Alterações - Aeronave {self.aircraft_title} - Data {self.date}"
    
@receiver(pre_save, sender=AicraftHistoric)
def update_titulo_aeronave(sender, instance, **kwargs):
    instance.aircraft_title = instance.aircraft.prefix


class Operation(Base):
    title = models.CharField(max_length=100)
    observer_pilot = models.ForeignKey(Military, on_delete=models.SET_NULL, related_name='operation_observer_pilot', blank=True, null=True)
    who_authorized = models.CharField(max_length=100, null=True, blank=True)
    who_requested = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(CitiesPB, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField("Latitude", default=0.0, null=False, blank=False)
    longitude = models.FloatField("Longitude", default=0.0, null=False, blank=False)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='operation_user', null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title


class TypeOfBattery(models.Model):
    name = models.CharField(max_length=45, null=False, default='', unique=True)
    recommended_cicles = models.IntegerField(null=False, default=45)
    alert_cicles = models.IntegerField(null=False, default=35)
    critical_cicles = models.IntegerField(null=False, default=50)
    
    def __str__(self):
        return f'{self.name}'


class Battery(Base):
    number = models.CharField(max_length=20, unique=True)
    num_cicles = models.IntegerField(null=False)
    maximum_cicles = models.ForeignKey(TypeOfBattery, on_delete=models.SET_NULL, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    battery_image = StdImageField(
        'Imagem',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True, null=True
    )

    def __str__(self):
        return self.number


class Checklist(Base):
    remote_pilot = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    num_propellers = models.IntegerField(default=4, null=False)
    num_batteries = models.IntegerField(default=4, null=False)
    batteries_loaded = models.BooleanField(default=True)
    control_battery_loaded = models.BooleanField(default=True)
    body = models.BooleanField(default=True)
    engine_rods = models.BooleanField(default=True)
    propellers = models.BooleanField(default=True)
    gimbal = models.BooleanField(default=True)
    spotlight = models.BooleanField(default=True)
    load_speaker = models.BooleanField(default=True)
    stroboscopic_light = models.BooleanField(default=True)
    cables = models.BooleanField(default=True) 
    charger = models.BooleanField(default=True)
    smart_controller = models.BooleanField(default=True)
    controller = models.BooleanField(default=True)
    sd_card = models.BooleanField(default=True)
    imu = models.BooleanField(default=True)
    compass = models.BooleanField(default=True)
    signal_transmission = models.BooleanField(default=True)
    system_rtk_ppk = models.BooleanField(default=True)
    video_signal = models.BooleanField(default=True)
    telemetry = models.BooleanField(default=True)
    parachute = models.BooleanField(default=True)
    changes = models.TextField()

    def __str__(self):
        return "Piloto: {} | {} | {} ".format(self.remote_pilot.military, self.aircraft, self.date)


class ChecklistImages(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    imageChecklist = StdImageField(
        'Imagem',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True, null=True
    )
     
     
class Report(Base):
    title = models.CharField(max_length=250, null=False, blank=False, default='')
    remote_pilot = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='report_remote_pilot', null=True)
    observer_pilot = models.ForeignKey(Military, on_delete=models.SET_NULL, related_name='report_observer_pilot', blank=True, null=True)
    who_authorized = models.CharField(max_length=100, null=True, blank=True)
    who_requested = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(blank=False, null=False)
    final_date = models.DateField(blank=True, null=True)
    initial_time = models.TimeField()
    final_time = models.TimeField(null=True)
    location = models.ForeignKey(CitiesPB, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField("Latitude", default=0.0, null=True, blank=True)
    longitude = models.FloatField("Longitude", default=0.0, null=True, blank=True)
    decea_request_file = models.FileField(
        upload_to='protocolos', storage=MinioBackend(
        bucket_name=settings.MINIO_MEDIA_FILES_BUCKET), 
        blank=True, 
        null=True)
    num_sarpas = models.CharField(max_length=20, blank=True, null=True)
    entity_support = models.ForeignKey(Entities, on_delete=models.SET_NULL, null=True)
    flight_nature = models.ForeignKey(FlightNature, on_delete=models.SET_NULL, null=True)
    type_of_operation = models.ForeignKey(TypesOfOperations, on_delete=models.SET_NULL, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    police_incident_number = models.CharField(max_length=100, null=True, blank=True, default='')
    operation_report = models.TextField(max_length=500)
    
    def __str__(self):
        return f'{self.title} - {self.remote_pilot.military.nickname} - {self.location}'


class Incidents(models.Model):
    operation = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    remote_pilot = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    report = models.TextField()
    location = models.ForeignKey(CitiesPB, on_delete=models.SET_NULL, null=True)
    reference_point = models.TextField()
    police_incident_number = models.CharField(max_length=100, null=True, blank=True, default='')
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.operation} | {self.date}'


class IncidentImage(models.Model):
    incident = models.ForeignKey(Incidents, on_delete=models.CASCADE)
    imageIncident = StdImageField(
        'Imagem',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True, null=True
    )

    
class PointsOfInterest(models.Model):
    operation = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    latitude = models.FloatField("Latitude", default=0.0, null=True, blank=True)
    longitude = models.FloatField("Longitude", default=0.0, null=True, blank=True)
    is_temporary = models.BooleanField(default=False)
    initial_date = models.DateTimeField(null=True, blank=True)
    final_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description


class Legislation(models.Model):
    title = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True, blank=True, default='')
    date_published = models.DateField(null=True)
    in_effect = models.BooleanField(default=True)
    legislation_file = models.FileField(
        upload_to='legislations', storage=MinioBackend(
        bucket_name=settings.MINIO_MEDIA_FILES_BUCKET), 
        blank=True, 
        null=True)
    
    def __str__(self):
        return f'{self.title} - {self.date_published}'
    
# risk analyses models
class Severity(models.Model):
    severity = models.CharField(max_length=1, null=False, default='')

    def __str__(self):
        return self.severity


class Probability(models.Model):
    probability = models.CharField(max_length=1, null=False, default='')

    def __str__(self):
        return self.probability
    
    
class Tolerability(models.Model):
    severity = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True)
    probability = models.ForeignKey(Probability, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.probability}{self.severity}"


class Situation(models.Model):
    situation = models.CharField(max_length=100, null=False, default='')
    
    def __str__(self):
        return self.situation

  
class RiskAssessment(models.Model):
    operational_scenario = models.CharField(max_length=300, null=False, default='')
    date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    operator = models.CharField(max_length=100, null=False, default='POLÍCIA MILITAR DO ESTADO DA PARAÍBA')
    cnpj = models.CharField(max_length=18, null=False, default='08.907.776/0001-00')
    aircrafts = models.ManyToManyField('Aircraft')
    apllied_legislation = models.TextField(
        null=False, 
        default='Lei nº 7.565/1986 – CBA; RBAC-E 94; ICA 100-40, MCA 56-5; IS nº E94-003')
    keep_distance_from_3rd = models.BooleanField(default=False)
    pilots_capabilities = models.BooleanField(default=True)
    accident_procedure = models.TextField(
        null=False, 
        default='Corpo de Bombeiros Militar da Paraíba, SAMU, Socorristas, Brigadistas. Deverá ser informado o ocorrido ao CIOP, solicitando o apoio necessário, ou procurar pelo responsável.')
    info_responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    responsible_sign = StdImageField(
        'Imagem',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True, null=True
    )

    def __str__(self):
        return f"{self.operational_scenario} - {self.operator} - {self.date}"
    
    
class Assessment(models.Model):
    situation = models.ForeignKey(Situation, on_delete=models.SET_NULL, null=True)
    probability_of_occurrence = models.ForeignKey(Probability, on_delete=models.SET_NULL, null=True)
    severity_of_occurrence = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True)
    risk = models.CharField(max_length=2, null=False, default='')
    hierarchy_authorization = models.CharField(max_length=100, null=True, blank=True)
    tolerability = models.CharField(max_length=100, null=False, default='')
    mitigation_measures_risk = models.TextField(null=False, default='')
    risk_assessment = models.ForeignKey(RiskAssessment, on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        self.risk = f"{self.probability_of_occurrence}{self.severity_of_occurrence}"
        
        risk_tolerance_mapping = {
            '4A': 'Risco extremo',
            '5A': 'Risco extremo',
            '5B': 'Risco extremo',
            '3A': 'Alto risco',
            '4B': 'Alto risco',
            '5C': 'Alto risco',
            '1A': 'Risco moderado',
            '2A': 'Risco moderado',
            '2B': 'Risco moderado',
            '3B': 'Risco moderado',
            '3C': 'Risco moderado',
            '4C': 'Risco moderado',
            '4D': 'Risco moderado',
            '5D': 'Risco moderado',
            '5E': 'Risco moderado',
            '1B': 'Baixo risco',
            '1C': 'Baixo risco',
            '2C': 'Baixo risco',
            '2D': 'Baixo risco',
            '3D': 'Baixo risco',
            '3E': 'Baixo risco',
            '4E': 'Baixo risco',
            '1D': 'Risco muito baixo',
            '1E': 'Risco muito baixo',
            '2E': 'Risco muito baixo',
        }
        self.tolerability = risk_tolerance_mapping.get(self.risk, 'Undefined')

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.situation.situation} - {self.risk_assessment}"