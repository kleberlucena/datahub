
from apps.rpa_manager.forms import MilitarForm
from apps.rpa_manager.models import Militar
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django_datatables_view.base_datatable_view import BaseDatatableView
from apps.portal.models import Promotion, HistoryTransfer, Military


class MilitaryListJson(BaseDatatableView):
    max_display_length = 100
    model = Military
    columns = ['id', 'rank', 'register', 'nickname', 'name',
               'cpf', 'activity_status', 'unidade']

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'rank':
            rank = Promotion.objects.filter(military=row.id).last()
            row.rank = rank.rank
            return row.rank

        if column == 'unidade':
            unit = HistoryTransfer.objects.filter(military=row.id).last()
            row.unidade = unit.entity.name
            return row.unidade

        return super(MilitaryListJson, self).render_column(row, column)


class VerEfetivoView(DetailView):
    model = Militar
    template_name = 'controle/pages/ver_efetivo.html'
    context_object_name = 'militar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        militar = self.get_object()
        roles = militar.roles.all()
        roles_as_strings = [str(role) for role in roles]

        context['roles'] = roles_as_strings
        return context

class CriarNovoMilitarView(CreateView):
    model = Militar
    form_class = MilitarForm
    template_name = 'controle/pages/criar_novo_militar.html'
    success_url = reverse_lazy('rpa_manager:efetivo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditarEfetivoView(UpdateView):
    model = Militar
    form_class = MilitarForm
    template_name = 'controle/pages/criar_novo_militar.html'
    success_url = reverse_lazy('rpa_manager:efetivo')
    context_object_name = 'militar'


class DeletarEfetivoView(DeleteView):
    model = Militar
    template_name = 'controle/pages/delete_efetivo.html'
    success_url = reverse_lazy('rpa_manager:efetivo')
    context_object_name = 'obj'