from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from . import tasks, models


class ImageListJson(BaseDatatableView):
    max_display_length = 100
    model = models.Image
    columns = ['uuid', "label", "file", "entity", "created_by", "created_at", "updated_at"]
    permission_required = 'image.view_image'


class ImageListView(TemplateView):
    template_name = 'image_list.html'
    # teste.delay()
    permission_required = 'image.view_image'


class TaskSetEntityFromImageView(TemplateView):
    template_name = 'process_task_set_entity_image.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromImageView,
                        self).get_context_data(**kwargs)
        task = tasks.task_set_entity_image.delay()
        context['task_id'] = task.id
        return context


class CommandsAPIImageView(TemplateView):
    template_name = 'command_image.html'