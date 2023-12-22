# Generated by Django 3.2.8 on 2023-12-22 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('details', models.CharField(blank=True, max_length=300, null=True, verbose_name='Descrição')),
            ],
        ),
    ]
