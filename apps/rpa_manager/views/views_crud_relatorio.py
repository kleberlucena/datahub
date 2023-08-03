from apps.rpa_manager.forms import RelatorioFormulario
from apps.rpa_manager.models import Missao, Relatorio
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from apps.rpa_manager.utils.create_json_for_coordinates import create_json_for_coordinates
from django.urls import reverse

class VerRelatorioView(DetailView):
    model = Relatorio
    template_name = 'controle/pages/ver_relatorio.html'
    context_object_name = 'relatorio'
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            relatorio = self.get_object()
            coordinates_json = {}
            context['coordinates_json'] = create_json_for_coordinates(coordinates_json, relatorio)

            return context
        
class CriarNovoRelatorioView(CreateView):
    model = Relatorio
    form_class = RelatorioFormulario
    template_name = 'controle/pages/criar_novo_relatorio.html'
    success_url = reverse_lazy('rpa_manager:add_point')
    
    def get_initial(self):
        missao = get_object_or_404(Missao, pk=self.kwargs['pk'])
        return {
            'titulo': missao.titulo,
            'militar': self.request.user,
            'piloto_observador': missao.piloto_observador,
            'quem_solicitou': missao.quem_solicitou,
            'quem_autorizou': missao.quem_autorizou,
            'local': missao.local,
            'latitude': missao.latitude,
            'longitude': missao.longitude,
            'relato_da_missao': 'Sem alteração',
            'aeronave': missao.aeronave,
        }
        
    def form_valid(self, form):
        self.object = self.get_context_data()
        evento_obj = form.save(commit=False)
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
    