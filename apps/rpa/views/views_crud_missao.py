from typing import Any, Dict
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from apps.rpa.forms import *
from apps.rpa.models import *
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from base.mixins import GroupRequiredMixin
from django.contrib import messages
import json
from django.utils.decorators import method_decorator
from django.utils.html import escape
from apps.rpa.handlers import require_permission
from apps.rpa.utils.getAttetionPointsForOperation import getAttentionPointsForOperation


class VerMissaoView(GroupRequiredMixin, DetailView):
    model = Operation
    template_name = 'rpa/detail_operation.html'
    context_object_name = 'missao'
    group_required = ['profile:rpa_view', 'profile:rpa_basic', 'profile:rpa_advanced']
     
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['latitude'] = str(self.object.latitude)
        context['longitude'] = str(self.object.longitude)
        return super().get_context_data(**kwargs)


class CriarNovaMissaoView(GroupRequiredMixin, View):
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get(self, request):
        form = OperationForm(initial={'user': request.user})
        aeronaves_disponiveis = Aircraft.objects.filter(in_use=False)
        
        points = PointsOfInterest.objects.all()
        points_list = getAttentionPointsForOperation(points)
        points_json = json.dumps(points_list, indent=4, ensure_ascii=False, default=str)
        
        availables_aircrafts = Aircraft.objects.filter(in_use=False).count()
        if(availables_aircrafts == 0):
            messages.info(request, 'Não há aeronaves disponíveis!')
            return redirect('rpa:principal')
        
        context = {
            'form': form,
            'points_json': points_json,
            'points': points,
            'aeronaves_disponiveis': aeronaves_disponiveis,
            }
        return render(request, 'rpa/create_operation.html', context)

    def post(self, request):
        form = OperationForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            missao = form.save(commit=False)
            aeronave = missao.aircraft
            aeronave.in_use = True
            aeronave.save()

            missao.save()
            
            messages.success(request, 'Operação criada com sucesso!')
            
            return redirect('rpa:principal')

        aeronaves_disponiveis = Aircraft.objects.filter(in_use=False)
        context = {'form': form,
                   'aeronaves_disponiveis': aeronaves_disponiveis}
        return render(request, 'rpa/create_operation.html', context)
    
    
class EditarMissaoView(GroupRequiredMixin, UpdateView):
    model = Operation
    form_class = OperationForm
    template_name = 'rpa/update_operation.html'
    context_object_name = 'form'
    success_url = reverse_lazy('rpa:principal')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        aeronave_anterior = self.object.aircraft

        if aeronave_anterior:
            aeronave_anterior.in_use = False
            aeronave_anterior.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        points = PointsOfInterest.objects.all()
            
        points_list = getAttentionPointsForOperation(points)
        points_json = json.dumps(points_list, indent=4, ensure_ascii=False, default=str)
        context['points_json'] = points_json
        context['points'] = points        
        return context
    
    def form_valid(self, form):
        missao = form.instance
        aeronave_anterior = missao.aircraft

        if aeronave_anterior:
            aeronave_anterior.in_use = False
            aeronave_anterior.save()

        response = super().form_valid(form)

        aeronave_nova = form.cleaned_data['aircraft']

        if aeronave_nova:
            aeronave_nova.in_use = True
            aeronave_nova.save()

        messages.success(self.request, 'Operação editada com sucesso!')
        
        return response

                
class DeleteMissaoView(GroupRequiredMixin, View):
    template_name = 'rpa/delete_operation.html'
    success_url = reverse_lazy('rpa:principal')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get(self, request, *args, **kwargs):
        missao = get_object_or_404(Operation, pk=self.kwargs['pk'])
        aeronave = missao.aircraft
        return render(request, self.template_name, {'missao': missao, 'aeronave': aeronave})
    
    def post(self, request, *args, **kwargs):
        missao = get_object_or_404(Operation, pk=self.kwargs['pk'])
        aeronave = missao.aircraft
        missao.delete()

        aeronave.in_use = False
        aeronave.save()

        messages.info(self.request, 'Operação excluída com sucesso!')
        
        return HttpResponseRedirect(self.success_url)
    
class OperationListJsonView(PermissionRequiredMixin, BaseDatatableView):
    print('chegou aqui')
    max_display_length = 100
    model = Operation
    columns = [
        'id',
        'title',
        'user',
        'date',
        'aircraft',
        'completed'
    ]
    permission_required = 'rpa.view_operation'

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'completed':
            # escape HTML for security reasons
            # return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
            if row.completed:
                return escape('{0}'.format('Encerrada'))
            else:
                return escape('{0}'.format('Em andamento'))
        else:
            return super(OperationListJsonView, self).render_column(row, column)

