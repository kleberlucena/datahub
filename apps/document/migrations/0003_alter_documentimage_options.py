# Generated by Django 3.2.8 on 2022-08-04 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_document_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentimage',
            options={'verbose_name': 'Imagem de documento', 'verbose_name_plural': 'Imagens de documento'},
        ),
    ]
