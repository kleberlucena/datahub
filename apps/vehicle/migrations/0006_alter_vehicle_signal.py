# Generated by Django 3.2.8 on 2023-02-23 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0005_auto_20230216_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='signal',
            field=models.CharField(max_length=11, unique=True, verbose_name='PLACA'),
        ),
    ]
