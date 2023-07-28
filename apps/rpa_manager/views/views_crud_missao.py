from django.shortcuts import redirect, render
from django.conf import settings
from django.shortcuts import get_object_or_404
from apps.rpa_manager.forms import MissaoFormulario
from apps.rpa_manager.models import Missao, Aeronave
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import (UpdateView,)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class VerMissaoView(LoginRequiredMixin, DetailView):
    model = Missao
    template_name = "controle/pages/ver_missao.html"
    context_object_name = 'missao'

    
class CriarNovaMissaoView(View):
    def get(self, request):
        form = MissaoFormulario(initial={'usuario': request.user})
        context = {'form': form}
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        # Verifica se a aeronave foi alterada
        aeronave_antiga_id = self.object.aeronave_id
        aeronave_nova_id = form.data['aeronave']
        if int(aeronave_antiga_id) != int(aeronave_nova_id):
            aeronave_antiga = Aeronave.objects.get(id=aeronave_antiga_id)
            aeronave_nova = Aeronave.objects.get(id=aeronave_nova_id)

            aeronave_antiga.em_uso = False
            aeronave_antiga.save()

            aeronave_nova.em_uso = True
            aeronave_nova.save()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
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

    