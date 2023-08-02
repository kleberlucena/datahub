from typing import Any, Dict
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa_manager.forms import BateriaForm
from apps.rpa_manager.models import Bateria


class VerBateriaView(DetailView):
    model = Bateria
    template_name = 'controle/pages/ver_bateria.html'
    context_object_name = 'bateria'
    pk_url_kwarg = 'pk'


class CriarNovaBateriaView(CreateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'controle/pages/criar_nova_bateria.html'
    success_url = reverse_lazy('rpa_manager:baterias')
    

class EditarBateriaView(UpdateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'controle/pages/editar_bateria.html'
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:baterias')


class DeletarBateriaView(DeleteView):
    model = Bateria
    template_name = 'controle/pages/delete_bateria.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:baterias')