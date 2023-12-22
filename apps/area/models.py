from django.db import models

class Area(models.Model):
    name = models.CharField("Nome", max_length=50)
    details = models.CharField("Descrição", max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name