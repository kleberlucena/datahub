# Generated by Django 3.2.8 on 2024-01-23 14:28

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0003_address_reference'),
        ('portal', '0022_alter_enjoyer_uuid_portal'),
        ('georeference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Ponto')),
                ('details', models.CharField(blank=True, max_length=300, null=True, verbose_name='Informações adicionais')),
                ('latitude', models.FloatField(default=0.0, verbose_name='Latitude')),
                ('longitude', models.FloatField(default=0.0, verbose_name='Longitude')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated_at', models.DateTimeField(verbose_name='Atualizado')),
                ('update_score', models.IntegerField(blank=True, null=True)),
                ('next_update', models.IntegerField(blank=True, null=True)),
                ('is_temporary', models.BooleanField(blank=True, default=False, null=True)),
                ('date_initial', models.DateTimeField(blank=True, null=True)),
                ('date_final', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Localização')),
                ('origin_system', models.CharField(default='bacinf', max_length=100, verbose_name='Sistema de origem')),
                ('origin_app', models.CharField(default='módulo de georeferenciamento', max_length=100, verbose_name='App de origem')),
            ],
        ),
        migrations.CreateModel(
            name='SpotType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Categoria')),
                ('update_time', models.IntegerField(default=30)),
                ('spot_type_father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spot_type_son', to='georeference.spottype', verbose_name='Categoria Pai')),
            ],
        ),
        migrations.CreateModel(
            name='SpotAddresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressType', models.CharField(blank=True, max_length=64, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='georef_spots_address', to='address.address')),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='georeference.spot')),
            ],
        ),
        migrations.AddField(
            model_name='spot',
            name='addresses',
            field=models.ManyToManyField(related_name='georef_spots_addresses', through='georeference.SpotAddresses', to='address.Address'),
        ),
        migrations.AddField(
            model_name='spot',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='georef_spots_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='spot',
            name='spot_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='georeference.spottype'),
        ),
        migrations.AddField(
            model_name='spot',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='georef_spots_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='spot',
            name='user_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='georef_spots_username', to='portal.enjoyer'),
        ),
        migrations.AddField(
            model_name='spot',
            name='user_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='georef_spots_entity', to='portal.entity'),
        ),
    ]
