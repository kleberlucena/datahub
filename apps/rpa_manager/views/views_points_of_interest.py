from django.views.generic import CreateView, UpdateView, DeleteView
from apps.rpa_manager.models import PontosDeInteresse, Relatorio
from apps.rpa_manager.forms import PointsOfInterestForm
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
    
    
class UpdatePointOfInterest(UpdateView):
    model = PontosDeInteresse
    form_class = PointsOfInterestForm
    template_name = 'controle/pages/edit_point.html'
    success_url = reverse_lazy('rpa_manager:criar_nova_missao')
    
    def get_initial(self):
        initial = super().get_initial()
        initial['operacao'] = self.object.operacao
        initial['latitude'] = self.object.latitude
        initial['longitude'] = self.object.longitude
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latitude'] = self.object.latitude
        context['longitude'] = self.object.longitude
        return context


class DeletePointOfInterest(DeleteView):
    model = PontosDeInteresse
    template_name = 'controle/pages/delete_point.html'
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:criar_nova_missao')