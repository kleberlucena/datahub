from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from apps.rpa_manager.forms import ChecklistForm
from apps.rpa_manager.models import Checklist
from django.urls import reverse_lazy

class VerChecklistView(DetailView):
    model = Checklist
    template_name = 'controle/pages/ver_checklist.html'
    context_object_name = 'checklist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_de_alteracoes = self.object.alteracoes.split('\n')
        nova_lista_alteracoes = []
        for item in lista_de_alteracoes:
            if len(lista_de_alteracoes) == 1 and lista_de_alteracoes[0] == '':
                nova_lista_alteracoes.append('Sem alterações')
            else:
                nova_lista_alteracoes.append(item + ' | ')
        context['nova_lista_alteracoes'] = nova_lista_alteracoes
        return context

class ChecklistFormView(CreateView):
    model = Checklist
    form_class = ChecklistForm
    template_name = 'controle/pages/checklist_form.html'
    success_url = reverse_lazy('controle:checklists')


class EditarChecklistView(UpdateView):
    model = Checklist
    form_class = ChecklistForm
    template_name = 'controle/pages/checklist_form.html'
    success_url = reverse_lazy('controle:checklists')
    context_object_name = 'checklist'
    extra_context = {'edicao_checklist': True}


class DeletarChecklistView(DeleteView):
    model = Checklist
    template_name = 'controle/pages/delete_checklist.html'
    success_url = reverse_lazy('controle:checklists')
    context_object_name = 'obj'
