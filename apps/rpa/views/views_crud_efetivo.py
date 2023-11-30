from apps.rpa.forms import *
from apps.rpa.models import *
from django.urls import reverse_lazy

from django_datatables_view.base_datatable_view import BaseDatatableView
from apps.portal.models import Entity, Military


class MilitaryListJson(BaseDatatableView):
    print(64*'#')
    print('no view_crud_efetivo')
    print(64*'#')
    max_display_length = 10
    model = Military
    columns = ['id', 'rank', 'register', 'nickname', 'name',
               'cpf', 'activity_status', 'unidade']

    def render_column(self, row, column):
        # We want to render military entity as a custom column
        if column == 'unidade':
            unit = Entity.objects.filter(military=row.id).last()
            row.unidade = unit.name
            return row.unidade

        return super(MilitaryListJson, self).render_column(row, column)