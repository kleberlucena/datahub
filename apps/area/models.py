from django.db import models

class Area(models.Model):
    name = models.CharField("Nome", max_length=50) #1BPM
    details = models.CharField("Descrição", max_length=300, null=True, blank=True) #Área do 1 Batalhão
    #cpr #CPRM
    #qpps = #QPP1,QPP2,QPP3,QPP4

    def __str__(self):
        return self.name
    

# class Qpp(models.Model):
#     name = models.CharField("Nome", max_length=50)
#     details = models.CharField("Descrição", max_length=300, null=True, blank=True)

#     def __str__(self):
#         return self.name
    

# class Cpr(models.Model):
#     name = models.CharField("Nome", max_length=50)
#     details = models.CharField("Descrição", max_length=300, null=True, blank=True)

#     def __str__(self):
#         return self.name