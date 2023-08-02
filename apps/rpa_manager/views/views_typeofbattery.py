from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from apps.rpa_manager.models import TypeOfBattery
from apps.rpa_manager.forms import TypeOfBatteryForm

class TypeOfBatteryCreateView(CreateView):
    model = TypeOfBattery
    form_class = TypeOfBatteryForm
    template_name = 'controle/pages/create_typeofbatteries.html' 
    success_url = reverse_lazy('rpa_manager:criar_nova_bateria')  

