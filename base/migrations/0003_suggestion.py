# Generated by Django 3.2.8 on 2023-03-14 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0014_alter_military_entity'),
        ('base', '0002_auto_20230119_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='Título')),
                ('content', models.TextField(verbose_name='Conteúdo')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggestion_creator', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='suggestion_entity', to='portal.entity')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggestion_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sugestão',
                'verbose_name_plural': 'Sugestões',
            },
        ),
    ]
