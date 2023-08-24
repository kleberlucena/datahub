
import json
from apps.rpa_manager.models import Missao

def getOperationInCourse():
    operationsInCourse = []
    
    operations = Missao.objects.filter(concluida=False)
    status_operation = None
    
    operationsNumber = operations.count()
    for operation in operations:
        if operation.concluida == False:
            status_operation = 'Em andamento'
        else:
            status_operation = ''
        
        if operations.exists() and operationsNumber > 0:
            operationsInCourse.append({
                'usuario': operation.usuario.username,
                'titulo': operation.titulo,
                'latitude': operation.latitude,
                'longitude': operation.longitude,
                'status': status_operation
            })
        else:
            return
    
    operationsInCourseJson = json.dumps(operationsInCourse, indent=4)
    
    return operationsInCourseJson
