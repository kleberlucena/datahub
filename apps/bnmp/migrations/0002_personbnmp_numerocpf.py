# Generated by Django 3.2.8 on 2023-01-11 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bnmp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personbnmp',
            name='numeroCPF',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
