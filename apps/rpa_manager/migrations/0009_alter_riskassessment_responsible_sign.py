# Generated by Django 3.2.8 on 2023-09-13 13:42

from django.db import migrations, models
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_manager', '0008_alter_riskassessment_responsible_sign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskassessment',
            name='responsible_sign',
            field=models.FileField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='bacinf-media'), upload_to='assinaturas'),
        ),
    ]
