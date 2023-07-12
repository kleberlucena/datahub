# Generated by Django 3.2.8 on 2023-07-12 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rpa_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aeronave',
            name='prefixo',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='bateria',
            name='numeracao',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='militar',
            name='matricula',
            field=models.CharField(max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='missao',
            name='piloto_observador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rpa_manager.militar'),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='militar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='piloto_observador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rpa_manager.militar'),
        ),
    ]
