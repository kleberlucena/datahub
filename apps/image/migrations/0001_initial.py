# Generated by Django 3.2.8 on 2022-08-29 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_minio_backend.models
import stdimage.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file', stdimage.models.StdImageField(storage=django_minio_backend.models.MinioBackend(bucket_name='bacinf-media'), upload_to='imagens', verbose_name='Imagem')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Imagem',
                'verbose_name_plural': 'Imagens',
            },
        ),
    ]
