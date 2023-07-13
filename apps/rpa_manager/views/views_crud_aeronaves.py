from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from apps.rpa_manager.forms import AeronavesForm
from apps.rpa_manager.models import Aeronave 


class VerAeronaveView(DetailView):
    model = Aeronave
    template_name = 'controle/pages/ver_aeronave.html'
    context_object_name = 'aeronave'
    pk_url_kwarg = 'pk'


class CriarNovaAeronaveView(CreateView):
    model = Aeronave
    form_class = AeronavesForm
    template_name = 'controle/pages/criar_nova_aeronave.html'
    success_url = reverse_lazy('rpa_manager:aeronaves')


class EditarAeronaveView(UpdateView):
    model = Aeronave
    form_class = AeronavesForm
    template_name = 'controle/pages/editar_aeronave.html'
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:aeronaves')

class DeletarAeronaveView(DeleteView):
    model = Aeronave
    template_name = 'controle/pages/delete_aeronave.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:aeronaves')