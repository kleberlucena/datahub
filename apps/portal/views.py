
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView

from . import models, tasks, services


class EntityListJson(BaseDatatableView):
    max_display_length = 100
    model = models.Entity
    columns = ['id', 'name', 'child_exists', 'category', 'hierarchy', 'created_at',
               'updated_at']
    # permission_required = 'entity.view_entity'


class EntityListView(TemplateView):
    template_name = 'entity_list.html'
    # teste.delay()
    # permission_required = 'entity.view_entity'


class ComandosAPIPortalView(TemplateView):
    template_name = 'command_portal.html'


class MilitaryListJson(BaseDatatableView):
    max_display_length = 100
    model = models.Military
    columns = ['id', 'rank', 'register', 'nickname', 'name',
               'cpf', 'activity_status', 'unidade']

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'rank':
            rank = models.Promotion.objects.filter(military=row.id).last()
            row.rank = rank.rank
            return row.rank

        if column == 'unidade':
            unit = models.HistoryTransfer.objects.filter(military=row.id).last()
            row.unidade = unit.entity.name
            return row.unidade

        return super(MilitaryListJson, self).render_column(row, column)


class MilitaryListView(TemplateView):
    template_name = 'military_list.html'


class MilitaryProfileView(DetailView):
    template_name = 'profile.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        object = get_object_or_404(models.Military, id=id_)
        promotions = models.Promotion.objects.filter(military=id_)
        object.rankActual = promotions.latest('created_at')
        object.promotions = promotions

        histories = models.HistoryTransfer.objects.filter(
            military=id_)
        object.histories = histories
        object.unitActual = histories.latest('created_at').entity.name

        return object


class SearchMilitaryView(TemplateView):
    template_name = 'search_military.html'
