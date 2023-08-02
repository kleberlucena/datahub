
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView

from .models import Entity, Promotion, HistoryTransfer
from .tasks import task_get_entity_from_portal, task_get_military_from_portal
from .services import *


class EntityListJson(BaseDatatableView):
    max_display_length = 100
    model = Entity
    columns = ['id', 'name', 'child_exists', 'category', 'hierarchy', 'created_at',
               'updated_at']
    # permission_required = 'entity.view_entity'


class EntityListView(TemplateView):
    template_name = 'entity_list.html'
    # teste.delay()
    # permission_required = 'entity.view_entity'


class TaskGetMilitaryFromPortalView(TemplateView):
    template_name = 'process_task_get_military_portal.html'

    def get_context_data(self, **kwargs):
        context = super(TaskGetMilitaryFromPortalView,
                        self).get_context_data(**kwargs)
        task = task_get_military_from_portal.delay()
        context['task_id'] = task.id
        return context


class TaskGetEntityFromPortalView(TemplateView):
    template_name = 'process_task_get_entity_portal.html'

    def get_context_data(self, **kwargs):
        context = super(TaskGetEntityFromPortalView,
                        self).get_context_data(**kwargs)
        task = task_get_entity_from_portal.delay()

        context['task_id'] = task.id
        return context

    # permission_required = 'entity.view_entity'


class ComandosAPIPortalView(TemplateView):
    template_name = 'command_portal.html'


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


class MilitaryListView(TemplateView):
    template_name = 'military_list.html'


class MilitaryProfileView(DetailView):
    template_name = 'profile.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        object = get_object_or_404(Military, id=id_)
        promotions = Promotion.objects.filter(military=id_)
        object.rankActual = promotions.latest('created_at')
        object.promotions = promotions

        histories = HistoryTransfer.objects.filter(
            military=id_)
        object.histories = histories
        object.unitActual = histories.latest('created_at').entity.name

        return object


class SearchMilitaryView(TemplateView):
    template_name = 'search_military.html'
