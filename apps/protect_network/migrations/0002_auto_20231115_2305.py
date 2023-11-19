# Generated by Django 3.2.8 on 2023-11-16 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_auto_20231115_2305'),
        ('protect_network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='responsibles',
            field=models.ManyToManyField(through='protect_network.NetworkResponsible', to='portal.Military'),
        ),
        migrations.AlterField(
            model_name='networkresponsible',
            name='responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.military'),
        ),
        migrations.AlterField(
            model_name='spot',
            name='user_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='spots', to='portal.military', verbose_name='Militar'),
        ),
    ]
