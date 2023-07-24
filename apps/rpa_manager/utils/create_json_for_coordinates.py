
import json

def create_json_for_coordinates(coordinates_dict, queryset):
    coordinates_dict['titulo'] = queryset.titulo
    coordinates_dict['latitude'] = queryset.latitude
    coordinates_dict['longitude'] = queryset.longitude

    return json.dumps(coordinates_dict)
