# Generated by Django 3.2.8 on 2023-08-20 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rpa_manager', '0031_auto_20230820_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guarnicao',
            name='piloto_observador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gu_piloto_observador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='guarnicao',
            name='piloto_remoto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gu_piloto_remoto', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='missao',
            name='piloto_observador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_piloto_observador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='missao',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
