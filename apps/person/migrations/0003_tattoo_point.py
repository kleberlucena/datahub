# Generated by Django 3.2.8 on 2022-09-13 13:57

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_rename_type_personaddresses_addresstype'),
    ]

    operations = [
        migrations.AddField(
            model_name='tattoo',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
