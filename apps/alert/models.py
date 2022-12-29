from django.db import models
from polymorphic.models import PolymorphicModel

class Alert(PolymorphicModel):



class VehicleAlert(Alert):
	car_id = models.AutoField(primary_key=True)
	latitudeocorrencia = models.CharField(max_length=100)
	imagem = models.CharField(max_length=100)
	datapassagem = models.CharField(max_length=100)
	unidaderegistrobo = models.CharField(max_length=100)
	nomedeclarante = models.CharField(max_length=100)
	sitocrid = models.CharField(max_length=100)
	dataocorrencia = models.CharField(max_length=100)
	longitudepassagem = models.CharField(max_length=100)
	municipioplaca = models.CharField(max_length=100)
	municipiolocal = models.CharField(max_length=100)
	longitudeocorrencia = models.CharField(max_length=100)
	latitudepassagem = models.CharField(max_length=100)
	telefonecontato = models.CharField(max_length=100)
	ufplaca = models.CharField(max_length=100)
	numerobo = models.CharField(max_length=100)
	uflocal = models.CharField(max_length=100)
	localpassagem = models.CharField(max_length=100)
	dddcontato = models.CharField(max_length=100)
	sisid = models.IntegerField()
	historicoocorrencia = models.CharField(max_length=100)
	idmovimento = models.CharField(max_length=100)
	placa = models.CharField(max_length=100)


class PersonAlert(Alert):
	person_id = models.AutoField(primary_key=True)
	estado = models.CharField(max_length=100)
	situacao = models.CharField(max_length=100)
	anobo = models.IntegerField()
	sistema = models.CharField(max_length=100)
	municipio = models.CharField(max_length=100)
	historico = models.CharField(max_length=100)
	nome = models.CharField(max_length=100)
	datahora = models.CharField(max_length=100)
	datanascimento = models.CharField(max_length=100)
	long = models.CharField(max_length=100)
	local = models.CharField(max_length=100)
	numeroocorrencia = models.CharField(max_length=100)
	uf = models.CharField(max_length=100)
	datahoraocorrencia = models.CharField(max_length=100)
	municipioocorrencia = models.CharField(max_length=100)
	foto = models.CharField(max_length=100)
	cpf = models.CharField(max_length=100)
	ufocorrencia = models.CharField(max_length=100)
	unidadeocorrencia = models.CharField(max_length=100)
	lat = models.CharField(max_length=100)
	sisid = models.CharField(max_length=100)
	nomemae = models.CharField(max_length=100)
	sitid = models.IntegerField()