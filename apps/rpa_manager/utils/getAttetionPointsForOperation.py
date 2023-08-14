from apps.rpa_manager.models import Missao, PontosDeInteresse
from django.utils import timezone
import pytz

def exclude_time_passed_points():
        tz = pytz.timezone('America/Recife')
        current_datetime = timezone.now().astimezone(tz)
        
        pontos_excluir = PontosDeInteresse.objects.filter(date_final__lte=current_datetime)
        
        pontos_excluir.delete()
        return tz

def getAttentionPointsForOperation(points):
    """O presente método recebe a queryset dos pontos de interesse
    e retorna uma lista com dicionários que possuem dados a
    serem renderizados no HTML em formato json.

    Args:
        points (_type_): queryset do django dos pontos de interesse

    Returns:
        list: lista com dicionários
    """
    
    points_list = []
    tz = exclude_time_passed_points()
    
    for point in points: 
        formatted_date_initial = None
        formatted_date_final = None

        if point.date_initial:
            formatted_date_initial = point.date_initial.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')
        
        if point.date_final:
            formatted_date_final = point.date_final.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S') 
            
        points_list.append({
                'temporary': point.is_temporary,
                'date_initial': formatted_date_initial or '',
                'date_final': formatted_date_final or '',
                'descricao': point.descricao,
                'latitude': point.latitude,
                'longitude': point.longitude,
                })
    
    return points_list