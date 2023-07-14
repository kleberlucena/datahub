from apps.rpa_manager.forms import RelatorioFormulario
from apps.rpa_manager.models import Missao, Relatorio
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

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
        missao = get_object_or_404(Missao, pk=self.kwargs['pk'])
        return {
            'titulo': missao.titulo,
            'militar': self.request.user,
            'piloto_observador': missao.piloto_observador,
            'local': missao.local,
            'relato_da_missao': 'Sem alteração',
            'aeronave': missao.aeronave,
        }

    def form_valid(self, form):
        missao = get_object_or_404(Missao, pk=self.kwargs['pk'])
        missao.concluida = True
        missao.save()

        aeronave = missao.aeronave
        aeronave.em_uso = False
        aeronave.save()

        form.instance.missao = missao
        return super().form_valid(form)

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
    