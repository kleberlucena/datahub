# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Gps

@shared_task
def clean_old_gps_data():
    # Calcule a data limite (7 dias atrás a partir do tempo atual)
    cutoff_date = timezone.now() - timezone.timedelta(days=30)

    # Remova registros com data de criação anterior à data limite
    deleted_count, _ = Gps.objects.filter(created_at__lt=cutoff_date).delete()
    return f'{deleted_count} registros Gps removidos com sucesso.'
