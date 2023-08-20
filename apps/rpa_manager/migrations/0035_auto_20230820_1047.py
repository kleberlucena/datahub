# Generated by Django 3.2.8 on 2023-08-20 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_manager', '0034_alter_relatorio_piloto_observador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missao',
            name='latitude',
            field=models.FloatField(default=0.0, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='missao',
            name='longitude',
            field=models.FloatField(default=0.0, verbose_name='Longitude'),
        ),
    ]
