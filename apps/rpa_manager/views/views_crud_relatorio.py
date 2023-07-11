from django.shortcuts import redirect, render

from . views_send_email import send_html_email
from apps.rpa_manager.forms import RelatorioFormulario
from apps.rpa_manager.models import Missao, Relatorio
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class VerRelatorioView(DetailView):
    model = Relatorio
    template_name = 'controle/pages/ver_relatorio.html'
    context_object_name = 'relatorio'


class CriarNovoRelatorioView(CreateView):
    model = Relatorio
    form_class = RelatorioFormulario
    template_name = 'controle/pages/criar_novo_relatorio.html'
    success_url = reverse_lazy('rpa_manager:relatorios')

    def get_initial(self):
        missao = Missao.objects.get(pk=self.kwargs['pk'])
        return {
            'titulo': missao.titulo,
            'militar': self.request.user,
            'piloto_observador': missao.piloto_observador,
            'data': missao.data,
            'local': missao.local,
            'relato_da_missao': 'Sem alteração',
            'aeronave': missao.aeronave
        }


class EditarRelatorioView(UpdateView):
    model = Relatorio
    form_class = RelatorioFormulario
    template_name = 'controle/pages/criar_novo_relatorio.html'
    success_url = reverse_lazy('rpa_manager:relatorios')
    context_object_name = 'relatorio'


class DeletarRelatorioView(DeleteView):
    model = Relatorio
    template_name = 'controle/pages/delete_relatorio.html'
    success_url = reverse_lazy('rpa_manager:relatorios')
    context_object_name = 'obj'
    