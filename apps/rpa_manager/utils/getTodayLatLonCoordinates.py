
import json
from datetime import datetime
from apps.rpa_manager.models import * 

def getTodaysCoordinates(context):
    operation_by_date_list = []
    status_operation = None

    today = datetime.now()
    month = today.month
    year = today.year
    
    try:
        operation_by_date = Operation.objects.filter(date__day=today.day, date__month=month, date__year=year)
    
        for operation in operation_by_date:
            if operation.completed == False:
                status_operation = 'Em andamento'
            else:
                status_operation = 'Encerrada'
                
            operation_by_date_list.append({
                'usuario': operation.user.military.nickname,
                'titulo': operation.title,
                'latitude': operation.latitude,
                'longitude': operation.longitude,
                'status': status_operation
            })
        
        today_coordinates_operations = json.dumps(operation_by_date_list, indent=4)
        return today_coordinates_operations
    except Exception as err:
        print(err)
