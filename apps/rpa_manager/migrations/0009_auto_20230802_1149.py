# Generated by Django 3.2.8 on 2023-08-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_manager', '0008_bateria_imagem_bateria'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeOfBattery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='bateria',
            name='maleta',
        ),
    ]
