from django.db import models

class Area(models.Model):
    name = models.CharField("Nome", max_length=50) #1BPM
    description = models.CharField("Descrição", max_length=300, null=True, blank=True) #Área do 1 Batalhão
    ####poligono delimitar a area

    def __str__(self):
        return self.name
