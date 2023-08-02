from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from . import tasks, models


class DocumentListJson(BaseDatatableView):
    max_display_length = 100
    model = models.Document
    columns = ['uuid', 'name', 'number', 'type', 'birth_date', 'mother', 'father',
                "entity", "created_by", "created_at", "updated_at"]
    permission_required = 'document.view_document'


class DocumentListView(TemplateView):
    template_name = 'document_list.html'
    permission_required = 'document.view_document'


class TaskSetEntityFromDocumentView(TemplateView):
    template_name = 'process_task_set_entity_document.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromDocumentView,
                        self).get_context_data(**kwargs)
        task = tasks.task_set_entity_document.delay()
        context['task_id'] = task.id
        return context


class CommandsAPIDocumentView(TemplateView):
    template_name = 'command_document.html'


class DocumentImageListJson(BaseDatatableView):
    max_display_length = 100
    model = models.DocumentImage
    columns = ['uuid', 'label', 'file', 'document', "entity", "created_by", "created_at", "updated_at"]
    permission_required = 'document.view_document_image'


class DocumentImageListView(TemplateView):
    template_name = 'document_image_list.html'
    permission_required = 'document.view_document_image'


class TaskSetEntityFromDocumentImageView(TemplateView):
    template_name = 'process_task_set_entity_document_image.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromDocumentImageView,
                        self).get_context_data(**kwargs)
        task = tasks.task_set_entity_document_image.delay()
        context['task_id'] = task.id
        return context


class CommandsAPIDocumentImageView(TemplateView):
    template_name = 'command_document_image.html'