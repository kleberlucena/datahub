
import json
from datetime import datetime
from apps.rpa_manager.models import Missao 

def getTodaysCoordinates(context):
    operation_by_date_list = []

    today = datetime.now()
    month = today.month
    year = today.year
    
    operation_by_date = Missao.objects.filter(data__day=today.day, data__month=month, data__year=year)
    
    for operation in operation_by_date:
        operation_by_date_list.append({
            'usuario': operation.usuario.username,
            'titulo': operation.titulo,
            'latitude': operation.latitude,
            'longitude': operation.longitude
        })
    
    today_coordinates_operations = json.dumps(operation_by_date_list, indent=4)
    return today_coordinates_operations