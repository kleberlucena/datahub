
import json

def create_json_for_coordinates(coordinates_dict: dict, queryset) -> json:
    coordinates_dict['usuario'] = queryset.militar.username
    coordinates_dict['titulo'] = queryset.titulo
    coordinates_dict['latitude'] = queryset.latitude
    coordinates_dict['longitude'] = queryset.longitude

    return json.dumps(coordinates_dict, indent=4, ensure_ascii=False)
