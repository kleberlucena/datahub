# Generated by Django 3.2.8 on 2023-01-03 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0002_alter_personalertcortex_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclealertcortex',
            name='imagem',
            field=models.TextField(blank=True, null=True),
        ),
    ]
