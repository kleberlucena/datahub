# Generated by Django 3.2.8 on 2023-03-03 18:24
from django.db import migrations

def set_new_column(apps, schema_editor):
    Military = apps.get_model('portal', 'Military')
    Entity = apps.get_model('portal', 'Entity')
    Vehicle = apps.get_model('vehicle', 'Vehicle')
    VehicleImage = apps.get_model('vehicle', 'VehicleImage')
    for row in Vehicle.objects.all():
        try:
            user = row.created_by
            entity = Military.objects.get(cpf=user.username).entity
            row.entity = entity
        except:
            row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
        row.save()
    for row in VehicleImage.objects.all():
        try:
            user = row.created_by
            entity = Military.objects.get(cpf=user.username).entity
            row.entity = entity
        except:
            row.entity = Entity.objects.get(name='PMPB|QCG|EME|EM 2')
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0008_auto_20230303_1520'),
    ]

    operations = [
        migrations.RunPython(set_new_column),
    ]