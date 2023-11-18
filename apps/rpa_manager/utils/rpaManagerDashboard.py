from apps.rpa_manager.models import *
from apps.portal.models import *
from django.core.exceptions import ObjectDoesNotExist
import json

class RpaManagerDashboard:
    def __init__(self):
        pass

    def get_max_pilot_operations(self):
        max_pilot_operations = {}

        try:
            militaries = Military.objects.all().select_related('user')  
        except Military.DoesNotExist as error:
            print(error)
            
        for military in militaries:
            try:
                number = Report.objects.filter(remote_pilot=military.user).count()
                max_pilot_operations[military] = number
            except Report.DoesNotExist:
                max_pilot_operations[military] = 0  

        return max_pilot_operations

    def get_amount_of_operations(self):
        try:
            reports = Report.objects.all().count()
            return reports
        except Report.DoesNotExist as error:
            print(error)
            
    def get_pilot_with_max_operations(self):
        try:
            return max(self.get_max_pilot_operations(), key=self.get_max_pilot_operations().get, default={})

        except ObjectDoesNotExist:
            return {}

    def get_number_of_pilot_max_oper(self):
        try:
            return max(self.get_max_pilot_operations().values(), default={})

        except ObjectDoesNotExist:
            return {}

    def get_most_supported_locations(self):
        try:
            most_supported_locations = {}
            
            cities = CitiesPB.objects.all()
            
            for city in cities:
                number = Report.objects.filter(location=city).count()
                most_supported_locations[city.cities_pb] = number
                
            return most_supported_locations
        except CitiesPB.DoesNotExist or Report.DoesNotExist as error:
            print(error)
            
    def get_most_supported_location(self):
        try:
            return max(self.get_most_supported_locations(), key=self.get_most_supported_locations().get, default={})

        except ObjectDoesNotExist:
            return {}

    def get_chart_data(self):
        try:
            most_supported_locations = self.get_most_supported_locations()
            sorted_locations = sorted(most_supported_locations.items(), key=lambda x: x[1], reverse=True)
            top_locations = sorted_locations[:5]

            labels = [location[0] for location in top_locations]
            data = [location[1] for location in top_locations]

            return json.dumps({'labels': labels, 'data': data})

        except Exception as e:
            print(f"Erro ao obter dados do gráfico: {e}")
            return json.dumps({'error': 'Ocorreu um erro ao obter dados do gráfico'})
    
    def get_operations_in_course(self):
        try:
            return Operation.objects.filter(completed=False).count()
        except ObjectDoesNotExist:
            return 0
    
    def get_available_aircrafts(self):
        try:
            return list(Aircraft.objects.filter(in_use=False))
        except ObjectDoesNotExist:
            return []
    
    def get_most_used_airctafts(self):
        most_used_aircrafts = {}
        
        try:
            aircrafts = Aircraft.objects.all()

            for aircraft in aircrafts:
                number = Report.objects.filter(aircraft=aircraft).count()
                most_used_aircrafts[f"{aircraft.prefix}"] = number
            
            return most_used_aircrafts

        except ObjectDoesNotExist:
            return {}

    
    def get_most_used_aircraft(self):
        try:
            most_used_aircrafts = self.get_most_used_airctafts()
            return max(most_used_aircrafts, key=most_used_aircrafts.get) or None

        except ObjectDoesNotExist:
            return None
    
    def get_batteries_cicles_level(self):
        try:
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

        except ObjectDoesNotExist:
            return json.dumps({'error': 'Ocorreu um erro ao obter informações da bateria'})
            