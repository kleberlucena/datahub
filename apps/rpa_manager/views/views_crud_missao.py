from typing import Any, Dict
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from apps.rpa_manager.forms import MissaoFormulario
from apps.rpa_manager.models import Missao, PontosDeInteresse
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from base.decorations.toast_decorator import include_toast
import json
from django.utils import timezone
import pytz
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission

def exclude_time_passed_points():
        tz = pytz.timezone('America/Recife')
        current_datetime = timezone.now().astimezone(tz)
        
        pontos_excluir = PontosDeInteresse.objects.filter(date_final__lte=current_datetime)
        
        pontos_excluir.delete()
        return tz

@include_toast
class VerMissaoView(PermissionRequiredMixin, DetailView):
    model = Missao
    template_name = "controle/pages/ver_missao.html"
    context_object_name = 'missao'
    permission_required = 'rpa_manager.view_missao'
        
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['latitude'] = str(self.object.latitude)
        context['longitude'] = str(self.object.longitude)
        return super().get_context_data(**kwargs)
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@include_toast
class CriarNovaMissaoView(PermissionRequiredMixin, View):
    permission_required = 'rpa_manager.add_missao'
    
    def get(self, request):
        form = MissaoFormulario(initial={'usuario': request.user})
        points_list = []
        points = PontosDeInteresse.objects.all()
        
        tz = exclude_time_passed_points()
        
        for point in points: 
            formatted_date_initial = None
            formatted_date_final = None

            if point.date_initial:
                formatted_date_initial = point.date_initial.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')
            
            if point.date_final:
                formatted_date_final = point.date_final.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')      
                     
            points_list.append({
                'temporary': point.is_temporary,
                'date_initial': formatted_date_initial or '',
                'date_final': formatted_date_final or '',
                'descricao': point.descricao,
                'latitude': point.latitude,
                'longitude': point.longitude,
                })
            
        points_json = json.dumps(points_list, indent=4, ensure_ascii=False, default=str)
        print(points_json)
        context = {
            'form': form,
            'points_json': points_json,
            'points': points,
            }
        return render(request, 'controle/pages/criar_nova_missao.html', context)

    def post(self, request):
        form = MissaoFormulario(request.POST, initial={'usuario': request.user})
        if form.is_valid():
            missao = form.save(commit=False)
            aeronave = missao.aeronave

            aeronave.em_uso = True
            aeronave.save()

            missao.save()
            
            messages.success(request, 'Operação criada com sucesso!')
            
            return redirect('rpa_manager:principal')

        context = {'form': form}
        return render(request, 'controle/pages/criar_nova_missao.html', context)
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class EditarMissaoView(PermissionRequiredMixin, UpdateView):
    model = Missao
    form_class = MissaoFormulario
    template_name = "controle/pages/editar_missao.html"
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:principal')
    permission_required = 'rpa_manager.change_missao'
    
    def get(self, request, *args, **kwargs):
        exclude_time_passed_points()
        
        self.object = self.get_object()

        aeronave_anterior = self.object.aeronave

        if aeronave_anterior:
            aeronave_anterior.em_uso = False
            aeronave_anterior.save()
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        missao = form.instance
        aeronave_anterior = missao.aeronave

        if aeronave_anterior:
            aeronave_anterior.em_uso = False
            aeronave_anterior.save()

        response = super().form_valid(form)

        aeronave_nova = form.cleaned_data['aeronave']

        if aeronave_nova:
            aeronave_nova.em_uso = True
            aeronave_nova.save()

        
        messages.success(self.request, 'Operação editada com sucesso!')
        
        return response

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
class DeleteMissaoView(PermissionRequiredMixin, View):
    template_name = "controle/pages/delete_mission.html"
    success_url = reverse_lazy('rpa_manager:principal')
    permission_required = 'rpa_manager.delete_missao'
    
    def get(self, request, *args, **kwargs):
        missao = get_object_or_404(Missao, pk=self.kwargs['pk'])
        aeronave = missao.aeronave
        return render(request, self.template_name, {'missao': missao, 'aeronave': aeronave})
    
    def post(self, request, *args, **kwargs):
        missao = get_object_or_404(Missao, pk=self.kwargs['pk'])
        aeronave = missao.aeronave
        missao.delete()

        aeronave.em_uso = False
        aeronave.save()

        messages.success(self.request, 'Operação excluída com sucesso!')
        
        return HttpResponseRedirect(self.success_url)

    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)