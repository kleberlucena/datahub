from apps.rpa_manager.models import *
from apps.portal.models import *
import json

class RpaManagerDashboard:
    def __init__(self):
        pass

    def get_max_pilot_operations(self):
        max_pilot_operations = {}

        militaries = Military.objects.all().select_related('user')

        for military in militaries:
            number = Report.objects.filter(remote_pilot=military.user).count()
            max_pilot_operations[military] = number

        return max_pilot_operations

    def get_amount_of_operations(self):
        return Report.objects.all().count() or None

    def get_pilot_with_max_operations(self):
        return max(self.get_max_pilot_operations(), key=self.get_max_pilot_operations().get) or None

    def get_number_of_pilot_max_oper(self):
        return max(self.get_max_pilot_operations().values()) or None  

    def get_most_supported_locations(self):
        most_supported_locations = {}
        
        cities = CitiesPB.objects.all()
        
        for city in cities:
            number = Report.objects.filter(location=city).count()
            most_supported_locations[city.cities_pb] = number
            
        return most_supported_locations
    
    def get_most_supported_location(self):
        return max(self.get_most_supported_locations(), key=self.get_most_supported_locations().get) or None
    
    
    def get_chart_data(self):
        most_supported_locations = self.get_most_supported_locations()
        sorted_locations = sorted(most_supported_locations.items(), key=lambda x: x[1], reverse=True)
        top_locations = sorted_locations[:5]

        labels = [location[0] for location in top_locations]
        data = [location[1] for location in top_locations]

        return json.dumps({'labels': labels, 'data': data})
    
    def get_operations_in_course(self):
        return Operation.objects.filter(completed=False).count()
    
    def get_available_aircrafts(self):
        return list(Aircraft.objects.filter(in_use=False))
    
    def get_most_used_airctafts(self):
        most_used_aircrafts = {}
        aircrafts = Aircraft.objects.all()
        
        for aircraft in aircrafts:
            number = Report.objects.filter(aircraft=aircraft).count()
            most_used_aircrafts[f"{aircraft.prefix}"] = number
            
        return most_used_aircrafts
    
    def get_most_used_aircraft(self):
        return max(self.get_most_used_airctafts(), key=self.get_most_used_airctafts().get) or None
    
    def get_batteries_cicles_level(self):
        batteries_info = []

        batteries = Battery.objects.all()

        for battery in batteries:
            battery_info = {
                'number': battery.number,
                'num_cicles': battery.num_cicles,
                'maximum_cicles': battery.maximum_cicles.recommended_cicles, 
            }

            batteries_info.append(battery_info)

        return json.dumps(batteries_info)
            