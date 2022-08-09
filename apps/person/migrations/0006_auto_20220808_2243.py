# Generated by Django 3.2.8 on 2022-08-09 01:43

from django.db import migrations
import django_minio_backend.models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0005_auto_20220808_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='face',
            name='image',
        ),
        migrations.AddField(
            model_name='face',
            name='file',
            field=stdimage.models.StdImageField(blank=True, storage=django_minio_backend.models.MinioBackend(bucket_name='bacinf-media'), upload_to='faces_imagens', verbose_name='Imagem'),
        ),
    ]
