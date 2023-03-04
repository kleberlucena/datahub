from django.db import models
from django.urls import reverse
from localflavor.br.models import BRStateField, BRCPFField, BRPostalCodeField

from django.utils import timezone


class Base(models.Model):
    created_at = models.DateField('Criado', auto_now_add=True)
    updated_at = models.DateField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class Entity(Base):
    ENTITY_CATEGORY = (
        (0, 'Outras Instituições'),
        (1, 'Polícia Militar da Paraíba - Ostensivo'),
        (2, 'Polícia Militar da Paraíba - Inteligência'),
        (3, 'Acessos Externo - Público Civil'),
    )
    ENTITY_HIERARCHY = (
        (0, 'Não definida'),
        (1, 'Comando Geral'),
        (2, 'Estado Maior Estratégico'),
        (3, 'Diretoria'),
        (4, 'Comando de Policiamento Regional'),
        (5, 'Batalhão Especializado'),
        (6, 'Batalhão'),
        (7, 'Companhia Independente'),
        (8, 'Companhia'),
        (9, 'Pelotão'),
        (10, 'Seção'),
        (11, 'Setor'),
        (12, 'Coordenação'),
        (13, 'Divisão Regional de Inteligência'),
        (14, 'Núcleo de Inteligência'),
        (15, 'Inteligência - Núcleos de Inteligência'),
    )
    name = models.CharField("Nome da entidade", max_length=100)
    father = models.CharField(
        "Código da entidade pai", max_length=7, default=0)
    child_exists = models.BooleanField("A entidade tem filhos?", default=False)
    category = models.IntegerField(
        "Tipo da entidade", default=0, choices=ENTITY_CATEGORY)
    hierarchy = models.IntegerField(
        "Hierarquia da entidade", default=0, choices=ENTITY_HIERARCHY)
    id_portal = models.IntegerField(
        "Id do Protal", default=0, unique=True)
    code = models.CharField("Código da entidade", max_length=7, unique=True)

    class Meta:
        verbose_name = 'Entidade'
        verbose_name_plural = 'Entidades'
        ordering = ['name']

    def __str__(self):
        return "{}".format(self.name)


class Military(Base):
    GENRE = (
        ('M', 'Masculino'),
        ('F', 'Feminino')
    )

    name = models.CharField("Nome completo", max_length=256, blank=False)
    url_image = models.CharField(
        "Endereço da imagem", max_length=256, blank=False)
    entity = models.ForeignKey(Entity, related_name='entity_military', on_delete=models.PROTECT)
    nickname = models.CharField("Nome de guerra", max_length=100, null=False)
    admission_date = models.DateField(
        "Data de admissão", blank=True, null=True)
    birthdate = models.DateField("Data de nascimento", blank=True, null=True)
    register = models.CharField("Matricula", max_length=7, blank=False)
    activity_status = models.CharField("Regime", max_length=100, blank=False)
    cpf = BRCPFField("CPF")
    genre = models.CharField("Gênero", max_length=1,
                             blank=False, choices=GENRE)
    email = models.CharField("Email", max_length=256, blank=False)
    father = models.CharField("Pai", max_length=256, blank=False)
    mather = models.CharField("Mãe", max_length=256, blank=False)
    place_of_birth = models.CharField(
        "Naturalidade", max_length=64, blank=False)
    marital_status = models.CharField(
        "Estado Civil", max_length=64, blank=False)
    phone = models.CharField("Telefone", max_length=36, blank=False)
    address = models.CharField("Endereço", max_length=256, blank=False)
    number = models.CharField("Número", max_length=16,
                              blank=False, default='S/N', null=False)
    complement = models.CharField("Complemento", max_length=100, blank=False)
    district = models.CharField("Bairro", max_length=100, blank=False)
    city = models.CharField("Cidade", max_length=100, blank=False)
    state = BRStateField("Estado")
    zipcode = BRPostalCodeField("CEP")
    unit = models.ManyToManyField(Entity, through='HistoryTransfer',)

    class Meta:
        unique_together = ('register', 'cpf',)
        verbose_name = 'Policial Militar'
        verbose_name_plural = 'Policiais Militares'

    def __str__(self):
        return self.nickname

#     def get_absolute_url(self):
#         return reverse('capabilities:add_student', kwargs={'pk': self.pk})


class HistoryTransfer(Base):
    entity = models.ForeignKey(Entity, verbose_name="Unidade", default=0, to_field='code', on_delete=models.CASCADE)
    military = models.ForeignKey(Military, on_delete=models.CASCADE)
    obs = models.CharField(max_length=255, blank=True, null=True)
    date_start = models.DateField('Data início', default=timezone.now)
    date_finish = models.DateField('Data fim', blank=True, null=True)

    class Meta:
        verbose_name = 'Transferência'
        verbose_name_plural = 'Transferências'

    def __str__(self):
        return "{} {}".format(self.entity, self.military)


class Promotion(Base):
    rank = models.CharField("Patente", max_length=36, blank=False)
    military = models.ForeignKey(Military, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Promoção'
        verbose_name_plural = 'Promoções'

    def __str__(self):
        return "{}".format(self.rank)
