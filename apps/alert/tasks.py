# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import VehicleAlertCortex, PersonAlertCortex

@shared_task
def clean_old_alerts_data():
    # Calcule a data limite (7 dias atrás a partir do tempo atual)
    cutoff_date = timezone.now() - timezone.timedelta(days=1000)

    # Remova registros com data de criação anterior à data limite
    deleted_vehicle_count, _ = VehicleAlertCortex.objects.filter(created_at__lt=cutoff_date).delete()
    deleted_person_count, _ = PersonAlertCortex.objects.filter(created_at__lt=cutoff_date).delete()
    return f'{deleted_person_count} registros de alertas de pessoas e {deleted_vehicle_count} registros de alertas de veículos removidos com sucesso.'
