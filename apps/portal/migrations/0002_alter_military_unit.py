# Generated by Django 3.2.8 on 2022-10-29 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='military',
            name='unit',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='portal.entity', to_field='code', verbose_name='Unidade'),
        ),
    ]
