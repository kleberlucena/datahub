from django.db import models

class Qpp(models.Model):
    name = models.CharField("QPP", max_length=50)
    details = models.CharField("Descrição", max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Cpr(models.Model):
    name = models.CharField("CPR", max_length=50)
    details = models.CharField("Descrição", max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name