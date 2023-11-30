from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from apps.rpa.models import TypeOfBattery
from apps.rpa.forms import TypeOfBatteryForm
from django.contrib import messages

MESSAGE_MODEL_NAME = 'Tipo de bateria'


class TypeOfBatteryCreateView(CreateView):
    model = TypeOfBattery
    form_class = TypeOfBatteryForm
    template_name = 'rpa/create_typeofbatteries.html'
    success_url = reverse_lazy('rpa:criar_nova_bateria')  

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criado com sucesso!')
        return response


class TypeOfBatteryUpdateView(UpdateView):
    model = TypeOfBattery
    form_class = TypeOfBatteryForm
    template_name = 'rpa/update_typeofbatteries.html'
    context_object_name = 'type_of_battery'
    success_url = reverse_lazy('rpa:typeofbatteries')  

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editado com sucesso!')
        return response


class TypeOfBatteryDeleteView(DeleteView):
    model = TypeOfBattery
    template_name = 'rpa/delete_typeofbatteries.html'
    context_object_name = 'type_of_battery'
    success_url = reverse_lazy('rpa:typeofbatteries') 
    context_object_name = 'obj'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluído com sucesso!')
        return response
