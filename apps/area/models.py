from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry


class Category(models.Model):
    name = models.CharField("Nome", max_length=50)
    description = models.CharField("Descrição", max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField("Nome", max_length=50)
    description = models.CharField("Descrição", max_length=300, null=True, blank=True)
    area_polygon = models.PolygonField("Área delimitada", null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    def get_centroid(self):
        # Verifica se o campo area_polygon está definido
        if self.area_polygon:
            # Calcula o centroide usando a biblioteca GEOSGeometry
            centroid = self.area_polygon.centroid
            return centroid
        else:
            return None  # Retorna None se não houver polígono definido
        


