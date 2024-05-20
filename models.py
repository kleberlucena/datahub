from django.db import models
from django.utils import timezone
from apps.georeference.models import Category, Area
from django.db import models, transaction
from django import forms

class SupportingNI(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OstensiveArresting(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OccurrenceNature(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class NiIndication(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DriRegion(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Incident(models.Model):
    CCD_key = models.CharField(max_length=12, unique=True, primary_key=True, editable=False)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    email_address = models.EmailField()
    occurrence_date = models.DateField()
    dri_region = models.ForeignKey(DriRegion, on_delete=models.CASCADE, related_name='incidents')
    ni_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="incidents", null=True)
    ni_indication = models.ManyToManyField(NiIndication, related_name="incidents")
    ostensive_arresting = models.ManyToManyField(OstensiveArresting, related_name="incidents")
    supporting_ni = models.ManyToManyField(SupportingNI, related_name="incidents")
    occurrence_nature = models.ForeignKey(OccurrenceNature, on_delete=models.CASCADE, related_name="incidents")
    

    def save(self, *args, **kwargs):
        if not self.CCD_key:
            with transaction.atomic():
                last_key = Incident.objects.select_for_update().order_by('-CCD_key').first()
                last_key_number = int(last_key.CCD_key[3:]) if last_key else 0
                new_number = last_key_number + 1
                self.CCD_key = f'CCD{str(new_number).zfill(7)}'
        super(Incident, self).save(*args, **kwargs)

    def __str__(self):
        return f'Incident on {self.occurrence_date} - {self.CCD_key}'

class Local(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='locals')
    endereco = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'Local for Incident {self.incident.CCD_key}'

class Guns(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='guns')
    guns_revolver = models.IntegerField(default=0)
    guns_pistol = models.IntegerField(default=0)
    guns_bpistol = models.IntegerField(default=0)
    guns_shotgun = models.IntegerField(default=0)
    guns_carbine = models.IntegerField(default=0)
    guns_mg = models.IntegerField(default=0)
    guns_rifle = models.IntegerField(default=0)
    guns_explosive = models.IntegerField(default=0)
    guns_clump = models.IntegerField(default=0)
    guns_handcrafted = models.IntegerField(default=0)
    guns_simulacrum = models.IntegerField(default=0)
    guns_ammunition = models.IntegerField(default=0)
    guns_bodyarmor = models.IntegerField(default=0)

    def __str__(self):
        return f'Guns for Incident {self.incident.CCD_key}'


class Vehicles(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='vehicles')
    recovered_car = models.IntegerField(default=0)
    recovered_moto = models.IntegerField(default=0)
    recovered_pickup = models.IntegerField(default=0)
    recovered_truck = models.IntegerField(default=0)
    recovered_other = models.IntegerField(default=0)
    administratively_seized_car = models.IntegerField(default=0)
    administratively_seized_moto = models.IntegerField(default=0)
    administratively_seized_pickup = models.IntegerField(default=0)
    administratively_seized_truck = models.IntegerField(default=0)
    administratively_seized_other = models.IntegerField(default=0)

    def __str__(self):
        return f'Vehicles for Incident {self.incident.CCD_key}'


class Drug(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='drugs')
    artane = models.IntegerField(default=0)
    lsd = models.IntegerField(default=0)
    ecstasy = models.IntegerField(default=0)
    lolo = models.IntegerField(default=0)
    crack = models.IntegerField(default=0)
    haxixe = models.IntegerField(default=0)
    tch = models.IntegerField(default=0)
    marihuana = models.IntegerField(default=0)
    skank = models.IntegerField(default=0)
    cocaine = models.IntegerField(default=0)

    def __str__(self):
        return f'Drug for Incident {self.incident.CCD_key}'


class Money(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='money')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'Money for Incident {self.incident.CCD_key}'
