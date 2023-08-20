
import json


def createJsonByLastOperation(coordinates_dict: dict, queryset) -> json:
    if queryset != None:
        coordinates_dict['usuario'] = queryset.usuario.username
        coordinates_dict['titulo'] = queryset.titulo
        coordinates_dict['latitude'] = queryset.latitude
        coordinates_dict['longitude'] = queryset.longitude

        return json.dumps(coordinates_dict, indent=4, ensure_ascii=False)
