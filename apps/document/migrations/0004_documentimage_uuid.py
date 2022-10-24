# Generated by Django 3.2.8 on 2022-10-24 13:36

from django.db import migrations, models
import uuid


def create_uuid(apps, schema_editor):
    document_image = apps.get_model('document', 'DocumentImage')
    for di in document_image.objects.all():
        di.uuid = uuid.uuid4()
        di.save()


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_alter_documenttype_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentimage',
            name='uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(create_uuid),
        migrations.AlterField(
            model_name='documentimage',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
