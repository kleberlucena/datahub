from django.shortcuts import redirect, render
from django.conf import settings
from django.shortcuts import get_object_or_404
from apps.rpa_manager.forms import MissaoFormulario
from apps.rpa_manager.models import Missao, PontosDeInteresse
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import (UpdateView,)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import json

class VerMissaoView(LoginRequiredMixin, DetailView):
    model = Missao
    template_name = "controle/pages/ver_missao.html"
    context_object_name = 'missao'

    
class CriarNovaMissaoView(View):
    def get(self, request):
        form = MissaoFormulario(initial={'usuario': request.user})
        points_list = []
        points = PontosDeInteresse.objects.all()
        for point in points:
            points_list.append({
                'descricao': point.descricao,
                'latitude': point.latitude,
                'longitude': point.longitude,
            })
            
        points_json = json.dumps(points_list, indent=4, ensure_ascii=False)
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
    

class EditarMissaoView(UpdateView):
    model = Missao
    form_class = MissaoFormulario
    template_name = "controle/pages/editar_missao.html"
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:principal')

    def get(self, request, *args, **kwargs):
        # Recuperar a missão atual
        self.object = self.get_object()
        # Recuperar a aeronave associada à missão antes da edição
        aeronave_anterior = self.object.aeronave
        # Definir o status da aeronave anterior como False, pois não será mais usada
        if aeronave_anterior:
            aeronave_anterior.em_uso = False
            aeronave_anterior.save()
        return super().get(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        # Recuperar a missão antes de atualizar os dados do formulário
        missao = form.instance

        # Recuperar a aeronave associada à missão antes da atualização
        aeronave_anterior = missao.aeronave

        # Definir o status da aeronave anterior como False, pois não será mais usada
        if aeronave_anterior:
            aeronave_anterior.em_uso = False
            aeronave_anterior.save()

        # Atualizar a missão com os dados do formulário
        response = super().form_valid(form)

        # Recuperar a nova aeronave selecionada no formulário de edição
        aeronave_nova = form.cleaned_data['aeronave']

        # Definir o status da nova aeronave selecionada como True
        if aeronave_nova:
            aeronave_nova.em_uso = True
            aeronave_nova.save()

        return response


        
class DeleteMissaoView(View):
    template_name = "controle/pages/delete_mission.html"
    success_url = reverse_lazy('rpa_manager:principal')

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

    