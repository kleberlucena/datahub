from typing import Any, Dict
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView
from apps.rpa_manager.models import PontosDeInteresse, Relatorio
from apps.rpa_manager.forms import PointsOfInterestForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class AddPointOfInterest(CreateView):
    model = PontosDeInteresse
    form_class = PointsOfInterestForm
    template_name = 'controle/pages/create_new_point.html'
    success_url = reverse_lazy('rpa_manager:painel')
    
    def get_initial(self):
            last_report = Relatorio.objects.last()
            return {
                'operacao': last_report,
                'latitude': last_report.latitude,
                'longitude': last_report.longitude
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_report = Relatorio.objects.last()
        context['latitude'] = last_report.latitude
        context['longitude'] = last_report.longitude
        return context