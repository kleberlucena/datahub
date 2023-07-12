from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa_manager.forms import BateriaForm
from apps.rpa_manager.models import Bateria


class VerBateriaView(DetailView):
    model = Bateria
    template_name = 'controle/pages/ver_bateria.html'
    context_object_name = 'bateria'
    pk_url_kwarg = 'id'


class CriarNovaBateriaView(CreateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'controle/pages/criar_nova_bateria.html'
    success_url = reverse_lazy('controle:baterias')


class EditarBateriaView(UpdateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'controle/pages/criar_nova_bateria.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('controle:baterias')


class DeletarBateriaView(DeleteView):
    model = Bateria
    template_name = 'controle/pages/delete_bateria.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('controle:baterias')