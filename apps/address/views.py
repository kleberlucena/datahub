from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from . import tasks, models


class AddressListJson(BaseDatatableView):
    max_display_length = 100
    model = models.Address
    columns = ['uuid', "street", "number", "complement", "neighborhood", "city",
                  "zipcode", "entity", "created_by", "created_at", "updated_at"]
    permission_required = 'address.view_address'

    """ def get_initial_queryset(self):
        return models.Address.objects.all().prefetch_related('nicknames') """


class AddressListView(TemplateView):
    template_name = 'address_list.html'
    # teste.delay()
    permission_required = 'address.view_address'


class TaskSetEntityFromAddressView(TemplateView):
    template_name = 'process_task_set_entity_address.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSetEntityFromAddressView,
                        self).get_context_data(**kwargs)
        task = tasks.task_set_entity_address.delay()
        context['task_id'] = task.id
        return context


class CommandsAPIAddressView(TemplateView):
    template_name = 'command_address.html'