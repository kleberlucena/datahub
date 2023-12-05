from apps.rpa.models import *
from django.utils import timezone
import pytz

def exclude_time_passed_points():
        tz = pytz.timezone('America/Recife')
        current_datetime = timezone.now().astimezone(tz)
        
        pontos_excluir = PointsOfInterest.objects.filter(final_date__lte=current_datetime)
        
        pontos_excluir.delete()
        return tz

def getAttentionPointsForOperation(points):
    points_list = []
    tz = exclude_time_passed_points()
    
    for point in points: 
        formatted_date_initial = None
        formatted_date_final = None

        if point.initial_date:
            formatted_date_initial = point.initial_date.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')
        
        if point.final_date:
            formatted_date_final = point.final_date.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S') 
            
        points_list.append({
                'temporary': point.is_temporary,
                'date_initial': formatted_date_initial or '',
                'date_final': formatted_date_final or '',
                'descricao': point.description,
                'latitude': point.latitude,
                'longitude': point.longitude,
                })
    
    return points_list