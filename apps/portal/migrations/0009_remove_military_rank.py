# Generated by Django 3.2.8 on 2022-11-08 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_promotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='military',
            name='rank',
        ),
    ]
