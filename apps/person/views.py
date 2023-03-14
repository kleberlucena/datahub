
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView

from apps.portal.models import Entity
from .models import Person, Tattoo
from .tasks import task_set_entity_person, task_set_entity_tattoo, task_set_entity_face, task_set_entity_physical, task_set_entity_nickname


class PersonListJson(BaseDatatableView):
    max_display_length = 100
    model = Entity
    columns = ['uuid', 'created_at', 'updated_at', 'entity',]
    # permission_required = 'entity.view_entity'


class PersonListView(TemplateView):
    template_name = 'person_list.html'
    # teste.delay()
    # permission_required = 'entity.view_entity'


class TaskSetEntityFromPersonView(TemplateView):
    template_name = 'process_task_set_entity_person.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromPersonView,
                        self).get_context_data(**kwargs)
        task = task_set_entity_person.delay()
        context['task_id'] = task.id
        return context


class TaskSetEntityFromTattooView(TemplateView):
    template_name = 'process_task_set_entity_tattoo.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromTattooView,
                        self).get_context_data(**kwargs)
        task = task_set_entity_tattoo.delay()

        context['task_id'] = task.id
        return context


class TaskSetEntityFromFaceView(TemplateView):
    template_name = 'process_task_set_entity_face.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromFaceView,
                        self).get_context_data(**kwargs)
        task = task_set_entity_face.delay()

        context['task_id'] = task.id
        return context


class TaskSetEntityFromPhysicalView(TemplateView):
    template_name = 'process_task_set_entity_physical.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromPhysicalView,
                        self).get_context_data(**kwargs)
        task = task_set_entity_physical.delay()

        context['task_id'] = task.id
        return context


class TaskSetEntityFromNicknameView(TemplateView):
    template_name = 'process_task_set_entity_nickname.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromNicknameView,
                        self).get_context_data(**kwargs)
        task = task_set_entity_nickname.delay()

        context['task_id'] = task.id
        return context


class ComandosAPIPersonView(TemplateView):
    template_name = 'command_person.html'


class TattooListJson(BaseDatatableView):
    max_display_length = 100
    model = Tattoo
    columns = ['id', 'uuid', 'label', 'point', 'file', 'medium', 'created_at', 'updated_at', 'entity']

    """ def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'rank':
            rank = Promotion.objects.filter(military=row.id).last()
            row.rank = rank.rank
            return row.rank

        if column == 'unidade':
            unit = HistoryTransfer.objects.filter(military=row.id).last()
            row.unidade = unit.entity.name
            return row.unidade

        return super(MilitaryListJson, self).render_column(row, column) """


class TattooListView(TemplateView):
    template_name = 'tattoo_list.html'


class PersonProfileView(DetailView):
    template_name = 'profile.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        object = get_object_or_404(Person, id=id_)
        """ promotions = Promotion.objects.filter(military=id_)
        object.rankActual = promotions.latest('created_at')
        object.promotions = promotions

        histories = HistoryTransfer.objects.filter(
            military=id_)
        object.histories = histories
        object.unitActual = histories.latest('created_at').entity.name """

        return object


class SearchPersonView(TemplateView):
    template_name = 'search_person.html'
