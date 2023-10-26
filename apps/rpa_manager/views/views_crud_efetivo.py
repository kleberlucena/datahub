from apps.rpa_manager.forms import *
from apps.rpa_manager.models import *
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