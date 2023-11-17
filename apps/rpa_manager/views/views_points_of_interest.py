from django.views.generic import CreateView, UpdateView, DeleteView
from apps.rpa_manager.models import *
from apps.rpa_manager.forms import *
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages

MESSAGE_MODEL_NAME = 'Ponto de atenção'

class AddPointOfInterest(CreateView):
    model = PointsOfInterest
    form_class = PointsOfInterestForm
    template_name = 'rpa_manager/create_point.html'
    success_url = reverse_lazy('rpa_manager:painel')
    
    def get_initial(self):
            last_report = Report.objects.last()
            return {
                'operacao': last_report,
                'latitude': last_report.latitude,
                'longitude': last_report.longitude
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_report = Report.objects.last()
        context['latitude'] = last_report.latitude
        context['longitude'] = last_report.longitude
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criado com sucesso!')
        return response
    
        
class UpdatePointOfInterest(UpdateView):
    model = PointsOfInterest
    form_class = PointsOfInterestForm
    template_name = 'rpa_manager/update_point.html'
    success_url = reverse_lazy('rpa_manager:criar_nova_missao')
        
    def get_initial(self):
        initial = super().get_initial()

        date_initial = self.object.initial_date
        date_final = self.object.final_date
        
        if date_initial and date_final:
            tz = timezone.pytz.timezone('America/Recife')
            initial['initial_date'] = date_initial.astimezone(tz)
            initial['final_date'] = date_final.astimezone(tz)
            return initial
        
        return
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latitude'] = self.object.latitude
        context['longitude'] = self.object.longitude

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editado com sucesso!')
        
        return response
    
    
class DeletePointOfInterest(DeleteView):
    model = PointsOfInterest
    template_name = 'rpa_manager/delete_point.html'
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:criar_nova_missao')
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluído com sucesso!')
        return response