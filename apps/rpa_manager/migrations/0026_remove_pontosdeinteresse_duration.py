# Generated by Django 3.2.8 on 2023-08-09 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_manager', '0025_auto_20230808_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pontosdeinteresse',
            name='duration',
        ),
    ]
