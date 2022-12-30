import uuid
from django.db import models
from polymorphic.models import PolymorphicModel

from apps.person.models import Person


class AlertCortex(PolymorphicModel):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	person = models.ForeignKey(Person, related_name='alerts', null=True, blank=True, on_delete=models.SET_NULL)
	dados = models.JSONField(null=True, blank=True)


class VehicleAlertCortex(AlertCortex):
	latitudeOcorrencia = models.CharField(max_length=100, null=True, blank=True)
	longitudeOcorrencia = models.CharField(max_length=100, null=True, blank=True)
	latitudePassagem = models.CharField(max_length=100, null=True, blank=True)
	longitudePassagem = models.CharField(max_length=100, null=True, blank=True)
	imagem = models.CharField(max_length=100, null=True, blank=True)
	dataPassagem = models.DateTimeField(max_length=100, null=True, blank=True)
	unidadeRegistroBo = models.CharField(max_length=100, null=True, blank=True)
	nomeDeclarante = models.CharField(max_length=100, null=True, blank=True)
	sitOcrId = models.CharField(max_length=100, null=True, blank=True)
	dataOcorrencia = models.DateTimeField(max_length=100, null=True, blank=True)
	municipioPlaca = models.CharField(max_length=100, null=True, blank=True)
	municipioLocal = models.CharField(max_length=100, null=True, blank=True)
	telefoneContato = models.CharField(max_length=100, null=True, blank=True)
	ufPlaca = models.CharField(max_length=100, null=True, blank=True)
	numeroBo = models.CharField(max_length=100, null=True, blank=True)
	ufLocal = models.CharField(max_length=100, null=True, blank=True)
	localPassagem = models.CharField(max_length=100, null=True, blank=True)
	dddContato = models.CharField(max_length=100, null=True, blank=True)
	sisId = models.IntegerField(null=True, blank=True)
	historicoOcorrencia = models.TextField(null=True, blank=True)
	idMovimento = models.CharField(max_length=100, null=True, blank=True)
	placa = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return f"{self.uuid}"

	class Meta:
		verbose_name = "Alerta Veículo"
		verbose_name_plural = "Alerta Veículos"


class PersonAlertCortex(AlertCortex):
	uf = models.CharField(max_length=100, null=True, blank=True)
	cpf = models.CharField(max_length=100, null=True, blank=True)
	nome = models.CharField(max_length=100, null=True, blank=True)
	nomeMae = models.CharField(max_length=100, null=True, blank=True)
	foto = models.CharField(max_length=100, null=True, blank=True)
	lat = models.CharField(max_length=100, null=True, blank=True)
	long = models.CharField(max_length=100, null=True, blank=True)
	estado = models.CharField(max_length=100, null=True, blank=True)
	situacao = models.CharField(max_length=100, null=True, blank=True)
	sistema = models.CharField(max_length=100, null=True, blank=True)
	municipio = models.CharField(max_length=100, null=True, blank=True)
	historico = models.TextField(null=True, blank=True)
	datahora = models.DateTimeField(max_length=100, null=True, blank=True)
	dataNascimento = models.DateField(max_length=100, null=True, blank=True)
	local = models.CharField(max_length=100, null=True, blank=True)
	anoBo = models.IntegerField(null=True, blank=True)
	numeroOcorrencia = models.CharField(max_length=100, null=True, blank=True)
	dataHoraOcorrencia = models.DateTimeField(max_length=100, null=True, blank=True)
	municipioOcorrencia = models.CharField(max_length=100, null=True, blank=True)
	ufOcorrencia = models.CharField(max_length=100, null=True, blank=True)
	unidadeOcorrencia = models.CharField(max_length=100, null=True, blank=True)
	sisId = models.CharField(max_length=100, null=True, blank=True)
	sitId = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return f"{self.uuid}"

	class Meta:
		verbose_name = "Alerta Pessoa"
		verbose_name_plural = "Alerta Pessoas"
