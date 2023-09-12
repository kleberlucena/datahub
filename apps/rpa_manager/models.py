import uuid
import string
import random
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend
from django.db.models.signals import pre_save
from django.dispatch import receiver

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


class Entidades(Base):
    entidade = models.CharField(max_length=100)

    def __str__(self):
        return self.entidade


class NaturezaDeVoo(Base):
    natureza = models.CharField(max_length=300)

    def __str__(self):
        return self.natureza


class TipoDeOperacao(Base):
    operacao = models.CharField(max_length=100)

    def __str__(self):
        return self.operacao


class CidadesPB(Base):
    cidades_pb = models.CharField(max_length=100)

    def __str__(self):
        return self.cidades_pb


class Guarnicao(models.Model):
    motorista = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='gu_motorista', null=True)
    piloto_remoto = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='gu_piloto_remoto', null=True)
    piloto_observador = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='gu_piloto_observador', blank=True, null=True)
    telefone = models.CharField(max_length=20, null=False, blank=False)
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.piloto_remoto} | {self.data} | {self.local}'
    
    
class Aeronave(Base):
    prefixo = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)
    em_uso = models.BooleanField(default=False, null=True, blank=True)
    imagem_aeronave = StdImageField(
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
        return "{} - {} - {}".format(self.prefixo, self.modelo, self.marca)


def generate_hex_code():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(25))

class HistoricoAlteracoesAeronave(models.Model):
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    titulo_aeronave = models.CharField(max_length=45, null=True)
    data = models.DateTimeField(default=timezone.now)
    codigo = models.CharField(max_length=25, unique=True, default=generate_hex_code)
    num_helices = models.IntegerField(default=4, null=False)
    num_baterias = models.IntegerField(default=4, null=False)
    baterias_carregadas = models.BooleanField(default=True)
    bateria_controle_carregada = models.BooleanField(default=True)
    corpo = models.BooleanField(default=True)
    hastes_motor = models.BooleanField(default=True)
    helices = models.BooleanField(default=True)
    gimbal = models.BooleanField(default=True)
    holofote = models.BooleanField(default=True)
    auto_falante = models.BooleanField(default=True)
    luz_estroboscopica = models.BooleanField(default=True)
    cabos = models.BooleanField(default=True)
    carregador = models.BooleanField(default=True)
    fonte = models.BooleanField(default=True)
    smart_controller = models.BooleanField(default=True)
    controle = models.BooleanField(default=True)
    cartao_sd = models.BooleanField(default=True)
    IMU = models.BooleanField(default=True)
    compass = models.BooleanField(default=True)
    sinal_transmissao = models.BooleanField(default=True)
    sistema_rtk_ppk = models.BooleanField(default=True)
    sinal_de_video = models.BooleanField(default=True)
    telemetria = models.BooleanField(default=True)
    paraquedas = models.BooleanField(default=True)
    alteracoes = models.TextField()

    def __str__(self):
        return f"Histórico de Alterações - Aeronave {self.titulo_aeronave} - Data {self.data}"
    
@receiver(pre_save, sender=HistoricoAlteracoesAeronave)
def update_titulo_aeronave(sender, instance, **kwargs):
    instance.titulo_aeronave = instance.aeronave.prefixo


class Missao(Base):
    titulo = models.CharField(max_length=100)
    piloto_observador = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='operation_piloto_observador', blank=True, null=True)
    quem_autorizou = models.CharField(max_length=100, null=True, blank=True)
    quem_solicitou = models.CharField(max_length=100, null=True, blank=True)
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField("Latitude", default=0.0, null=False, blank=False)
    longitude = models.FloatField("Longitude", default=0.0, null=False, blank=False)
    horario = models.TimeField(auto_now_add=True)
    data = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='operation_usuario', null=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    concluida = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.titulo


class TypeOfBattery(models.Model):
    name = models.CharField(max_length=45, null=False, default='', unique=True)
    recommended_cicles = models.IntegerField(null=False, default=45)
    alert_cicles = models.IntegerField(null=False, default=35)
    critical_cicles = models.IntegerField(null=False, default=50)
    
    def __str__(self):
        return f'{self.name}'


class Bateria(Base):
    numeracao = models.CharField(max_length=20, unique=True)
    num_ciclos = models.IntegerField(null=False)
    ciclos_maximo = models.ForeignKey(TypeOfBattery, on_delete=models.SET_NULL, null=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    imagem_bateria = StdImageField(
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
        return self.numeracao


class Checklist(Base):
    piloto = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    horario = models.TimeField(auto_now_add=True)
    data = models.DateField(auto_now_add=True)
    num_helices = models.IntegerField(default=4, null=False)
    num_baterias = models.IntegerField(default=4, null=False)
    baterias_carregadas = models.BooleanField(default=True)
    bateria_controle_carregada = models.BooleanField(default=True)
    corpo = models.BooleanField(default=True)
    hastes_motor = models.BooleanField(default=True)
    helices = models.BooleanField(default=True)
    gimbal = models.BooleanField(default=True)
    holofote = models.BooleanField(default=True)
    auto_falante = models.BooleanField(default=True)
    luz_estroboscopica = models.BooleanField(default=True)
    cabos = models.BooleanField(default=True)
    carregador = models.BooleanField(default=True)
    fonte = models.BooleanField(default=True)
    smart_controller = models.BooleanField(default=True)
    controle = models.BooleanField(default=True)
    cartao_sd = models.BooleanField(default=True)
    IMU = models.BooleanField(default=True)
    compass = models.BooleanField(default=True)
    sinal_transmissao = models.BooleanField(default=True)
    sistema_rtk_ppk = models.BooleanField(default=True)
    sinal_de_video = models.BooleanField(default=True)
    telemetria = models.BooleanField(default=True)
    paraquedas = models.BooleanField(default=True)
    alteracoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Piloto: {} | {} | {} ".format(self.piloto, self.aeronave, self.data)

class ImagensChecklist(models.Model):
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
     
class Relatorio(Base):
    titulo = models.CharField(max_length=250, null=False, blank=False, default='')
    militar = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='report_militar', null=True)
    piloto_observador = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='report_piloto_observador', blank=True, null=True)
    quem_autorizou = models.CharField(max_length=100, null=True, blank=True)
    quem_solicitou = models.CharField(max_length=100, null=True, blank=True)
    data = models.DateField(blank=False, null=False)
    data_final = models.DateField(blank=True, null=True)
    horario_inicial = models.TimeField()
    horario_final = models.TimeField()
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField("Latitude", default=0.0, null=True, blank=True)
    longitude = models.FloatField("Longitude", default=0.0, null=True, blank=True)
    arquivo_solicitacao = models.FileField(
        upload_to='protocolos', storage=MinioBackend(
        bucket_name=settings.MINIO_MEDIA_FILES_BUCKET), 
        blank=True, 
        null=True)
    num_sarpas = models.CharField(max_length=20, blank=True, null=True)
    entidade_apoiada = models.ForeignKey(Entidades, on_delete=models.SET_NULL, null=True)
    natureza_de_voo = models.ForeignKey(NaturezaDeVoo, on_delete=models.SET_NULL, null=True)
    tipo_de_operacao = models.ForeignKey(TipoDeOperacao, on_delete=models.SET_NULL, null=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    numero_ficha_oc = models.CharField(max_length=100, null=True, blank=True, default='')
    relato_da_missao = models.TextField(max_length=500)
    
    def __str__(self):
        return f'{self.titulo} - {self.militar} - {self.local}'


class Incidentes(models.Model):
    operacao = models.ForeignKey(Relatorio, on_delete=models.SET_NULL, null=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    piloto = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    relato = models.TextField()
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)
    ponto_de_referencia = models.TextField()
    data = models.DateTimeField()

    def __str__(self):
        return f'{self.operacao} | {self.data}'


class ImagensIncidente(models.Model):
    incidente = models.ForeignKey(Incidentes, on_delete=models.CASCADE)
    imageIncidente = StdImageField(
        'Imagem',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True, null=True
    )

    
class PontosDeInteresse(models.Model):
    operacao = models.ForeignKey(Relatorio, on_delete=models.SET_NULL, null=True)
    descricao = models.TextField()
    latitude = models.FloatField("Latitude", default=0.0, null=True, blank=True)
    longitude = models.FloatField("Longitude", default=0.0, null=True, blank=True)
    is_temporary = models.BooleanField(default=False)
    date_initial = models.DateTimeField(null=True, blank=True)
    date_final = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.descricao


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
    aircrafts = models.ManyToManyField('Aeronave')
    apllied_legislation = models.TextField(
        null=False, 
        default='Lei nº 7.565/1986 – CBA; RBAC-E 94; ICA 100-40, MCA 56-5; IS nº E94-003')
    keep_distance_from_3rd = models.BooleanField(default=False)
    pilots_capabilities = models.BooleanField(default=True)
    accident_procedure = models.TextField(
        null=False, 
        default='Corpo de Bombeiros Militar da Paraíba, SAMU, Socorristas, Brigadistas. Deverá ser informado o ocorrido ao CIOP, solicitando o apoio necessário, ou procurar pelo responsável.')
   

    def __str__(self):
        return f"{self.operational_scenario} - {self.operator} - {self.date}"
    
    
class Assessment(models.Model):
    situation = models.ForeignKey(Situation, on_delete=models.SET_NULL, null=True)
    probability_of_occurrence = models.ForeignKey(Probability, on_delete=models.SET_NULL, null=True)
    severity_of_occurrence = models.ForeignKey(Severity, on_delete=models.SET_NULL, null=True)
    risk = models.CharField(max_length=2, null=False, default='')
    hierarchy_authorization = models.CharField(max_length=100, null=True, blank=True)
    tolerability = models.CharField(max_length=100, null=False, default='')
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