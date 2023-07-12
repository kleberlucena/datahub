import uuid
from django.contrib.auth.models import User
from django.db import models

class Base(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True
    
class OPM(Base):
    opm = models.CharField(max_length=100)

    def __str__(self):
        return self.opm

class Unidades(Base):
    unidades = models.CharField(max_length=100)

    def __str__(self):
        return self.unidades

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

class Roles(Base):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role
    
class Militar(Base):  
    nome_de_guerra = models.CharField(max_length=100, null=False)
    total_de_horas_voo = models.IntegerField(default=0, null=False)
    matricula = models.CharField(max_length=9, null=False, unique=True)
    roles = models.ManyToManyField('Roles')

    def __str__(self):
        return self.nome_de_guerra

class Maleta(Base):
    nome = models.CharField(max_length=20)
    num_baterias = models.IntegerField(null=False)
    controle = models.IntegerField(null=False)
    fonte = models.IntegerField(null=False)
    hub = models.IntegerField(null=False)
    cabo_usb = models.IntegerField(null=False)
    cabo_energia = models.IntegerField(null=False)
    helices = models.IntegerField(null=False)
    
    def __str__(self):
        return self.nome


class Aeronave(Base):
    prefixo = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    maleta = models.ForeignKey(Maleta, on_delete=models.SET_NULL, null=True)
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.prefixo


class Missao(Base):
    titulo = models.CharField(max_length=100)
    piloto_observador = models.ForeignKey(Militar, on_delete=models.SET_NULL, blank=True, null=True)
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)
    horario = models.TimeField(auto_now_add=True)
    data = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    concluida = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.titulo


class Bateria(Base):
    numeracao = models.CharField(max_length=20, unique=True)
    num_ciclos = models.IntegerField(null=False)
    ciclos_maximo = models.IntegerField(null=False, default=45)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    maleta = models.ForeignKey(Maleta, on_delete=models.SET_NULL, null=True)

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


class Relatorio(Base):
    titulo = models.CharField(max_length=250, null=False, blank=False, default='')
    militar = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    piloto_observador = models.ForeignKey(Militar, on_delete=models.SET_NULL, blank=True, null=True)
    data = models.DateField(blank=False, null=False)
    horario_inicial = models.TimeField()
    horario_final = models.TimeField()
    local = models.ForeignKey(CidadesPB, on_delete=models.SET_NULL, null=True)
    arquivo_solicitacao = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    num_sarpas = models.CharField(max_length=20, blank=True, null=True)
    opm_apoiada = models.ForeignKey(OPM, on_delete=models.SET_NULL, null=True)
    unidade_apoiada = models.ForeignKey(Unidades, on_delete=models.SET_NULL, null=True)
    natureza_de_voo = models.ForeignKey(NaturezaDeVoo, on_delete=models.SET_NULL, null=True)
    tipo_de_operacao = models.ForeignKey(TipoDeOperacao, on_delete=models.SET_NULL, null=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True)
    relato_da_missao = models.TextField(max_length=500)
    
    def __str__(self):
        return self.titulo

