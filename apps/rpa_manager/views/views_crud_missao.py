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


def exclude_time_passed_points():
    # Configura o fuso horário "America/Recife"
        tz = pytz.timezone('America/Recife')
        current_datetime = timezone.now().astimezone(tz)
        
        # Filtra e exclui objetos cuja data final é menor ou igual à data e hora atual
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
    

@include_toast
class CriarNovaMissaoView(PermissionRequiredMixin, View):
    permission_required = 'rpa_manager.add_missao'
    
    def get(self, request):
        form = MissaoFormulario(initial={'usuario': request.user})
        points_list = []
        points = PontosDeInteresse.objects.all()
        
        tz = exclude_time_passed_points()
        
        def format_time_for_json():
            for point in points:
                if point.date_initial and point.date_final:
                    formatted_date_initial = point.date_initial.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')
                    formatted_date_final = point.date_final.astimezone(tz).strftime('%d/%m/%Y %H:%M:%S')
            return {'date_inicial': formatted_date_initial, 'date_final': formatted_date_final}
        
        for point in points:            
            points_list.append({
                'temporary': point.is_temporary,
                'date_initial': format_time_for_json()['date_inicial'] or '',
                'date_final': format_time_for_json()['date_final'] or '',
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
            return redirect('rpa_manager:principal')

        context = {'form': form}
        return render(request, 'controle/pages/criar_nova_missao.html', context)
    
class EditarMissaoView(PermissionRequiredMixin, UpdateView):
    model = Missao
    form_class = MissaoFormulario
    template_name = "controle/pages/editar_missao.html"
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:principal')
    permission_required = 'rpa_manager.edit_missao'

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

        return response

        
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

        # Exclui a missão
        missao.delete()

        # Atualiza o status da aeronave para False
        aeronave.em_uso = False
        aeronave.save()

        return HttpResponseRedirect(self.success_url)

    