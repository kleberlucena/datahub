# Generated by Django 3.2.8 on 2023-08-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_manager', '0013_alter_typeofbattery_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoalteracoesaeronave',
            name='titulo_aeronave',
            field=models.CharField(max_length=45, null=True, unique=True),
        ),
    ]
