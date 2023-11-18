
import json
from apps.rpa_manager.models import *

def getOperationInCourse():
    operationsInCourse = []
    
    operations = Operation.objects.filter(completed=False)
    status_operation = None
    
    operationsNumber = operations.count()
    for operation in operations:
        if operation.completed == False:
            status_operation = 'Em andamento'
        else:
            status_operation = 'Encerrada'
        
        if operations.exists() and operationsNumber > 0:
            operationsInCourse.append({
                'usuario': operation.user.military.nickname,
                'titulo': operation.title,
                'latitude': operation.latitude,
                'longitude': operation.longitude,
                'status': status_operation
            })
        else:
            return
    
    operationsInCourseJson = json.dumps(operationsInCourse, indent=4)
    
    return operationsInCourseJson
