
import json


def createJsonByLastOperation(coordinates_dict: dict, queryset) -> json:
    if queryset != None:
        print("######### is not NONE")
        print("######### {queryset}")
        coordinates_dict['usuario'] = queryset.user.username
        coordinates_dict['titulo'] = queryset.title
        coordinates_dict['latitude'] = queryset.latitude
        coordinates_dict['longitude'] = queryset.longitude

        return json.dumps(coordinates_dict, indent=4, ensure_ascii=False)
    
    else:
        print("######### is NONE")
        return {}
