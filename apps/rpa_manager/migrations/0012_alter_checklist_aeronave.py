# Generated by Django 3.2.8 on 2023-07-25 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpa_manager', '0011_auto_20230724_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='aeronave',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rpa_manager.aeronave'),
        ),
    ]
