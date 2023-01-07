import datetime
from django.db import migrations

def set_created_at_default(apps, schema_editor):
    AlertCortex = apps.get_model('alert', 'AlertCortex')
    default_value = datetime.datetime.now()
    AlertCortex.objects.update(created_at=default_value)

class Migration(migrations.Migration):
    dependencies = [
        ('alert', '0006_alertcortex_created_at'),
    ]
    operations = [
        migrations.RunPython(set_created_at_default),
    ]