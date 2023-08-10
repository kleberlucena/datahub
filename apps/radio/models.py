from django.contrib.gis.db import models
import uuid

# Create your models here.
class Gps(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    location = models.PointField(srid=4326, null=True, blank=True)
    accuracy = models.IntegerField()
    emergency = models.BooleanField()
    timestamp = models.DateTimeField()
    id = models.CharField(max_length=20, primary_key=False)
    timestampReceived = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "gps"
        verbose_name_plural = "gps"
