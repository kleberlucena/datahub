
from apps.rpa_manager.forms import MilitarForm
from apps.rpa_manager.models import Militar
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class VerEfetivoView(DetailView):
    model = Militar
    template_name = 'controle/pages/ver_efetivo.html'
    context_object_name = 'militar'

class CriarNovoMilitarView(CreateView):
    model = Militar
    form_class = MilitarForm
    template_name = 'controle/pages/criar_novo_militar.html'
    success_url = reverse_lazy('controle:efetivo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_app_page'] = True
        return context


class EditarEfetivoView(UpdateView):
    model = Militar
    form_class = MilitarForm
    template_name = 'controle/pages/criar_novo_militar.html'
    success_url = reverse_lazy('controle:efetivo')
    context_object_name = 'militar'


class DeletarEfetivoView(DeleteView):
    model = Militar
    template_name = 'controle/pages/delete_efetivo.html'
    success_url = reverse_lazy('controle:efetivo')
    context_object_name = 'obj'