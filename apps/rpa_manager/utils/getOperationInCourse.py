
import json
from apps.rpa_manager.models import Missao

def getOperationInCourse():
    operationsInCourse = []
    
    operations = Missao.objects.filter(concluida=False)
    
    operationsNumber = operations.count()
    for operation in operations:
        if operations.exists() and operationsNumber > 0:
            operationsInCourse.append({
                'usuario': operation.usuario.username,
                'titulo': operation.titulo,
                'latitude': operation.latitude,
                'longitude': operation.longitude
            })
        else:
            return
    
    operationsInCourseJson = json.dumps(operationsInCourse, indent=4)
    
    return operationsInCourseJson
