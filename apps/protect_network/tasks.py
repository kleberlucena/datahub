from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import ProtectNetworkSpot
import math



@shared_task
def task_update_scores():
    spots = ProtectNetworkSpot.objects.all()

    for spot in spots:
        total_update_interval = timedelta(days=spot.spot.spot_type.update_time).total_seconds()
        passed_update_interval = (timezone.now() - spot.spot.updated_at).total_seconds()
        update_score = (1 - (passed_update_interval / total_update_interval)) * 100
        spot.update_score = round(update_score)        
        spot.save()

        # Calculating time until next update
        update_interval = timedelta(days=spot.spot.spot_type.update_time)
        next_update_date = spot.spot.updated_at + update_interval
        time_until_update = next_update_date - timezone.now()
        time_until_update_days = math.ceil(time_until_update.total_seconds() / (24 * 3600))
        spot.next_update = time_until_update_days
        spot.save()
