from django.shortcuts import redirect, render
from django.conf import settings

from . views_send_email import send_html_email
from apps.rpa_manager.forms import MissaoFormulario
from apps.rpa_manager.models import Missao
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import (CreateView, UpdateView,
                                       DeleteView,)

def ver_missao(request, id):
    missao = Missao.objects.get(pk=id)
    
    return render(request, 'controle/pages/ver_missao.html', {'missao': missao})

    
class CriarNovaMissaoView(View):
    def get(self, request):
        form = MissaoFormulario(initial={'usuario': request.user})
        context = {'form': form}
        return render(request, 'controle/pages/criar_nova_missao.html', context)

    def post(self, request):
        form = MissaoFormulario(request.POST, initial={'usuario': request.user})
        if form.is_valid():
            form.save()
            return redirect('rpa_manager:principal')

        context = {'form': form}
        return render(request, 'controle/pages/criar_nova_missao.html', context)


# def editar_missao(request, id):
#     missao = Missao.objects.get(pk=id)
#     missao_form = MissaoFormulario(instance=missao)
    
#     if request.method == 'POST':
#         missao_form =  MissaoFormulario(request.POST, instance=missao)
#         if missao_form.is_valid():
#             missao_form.save()
#             return redirect('rpa_manager:principal')

#     context = {'missao_form': missao_form}
#     return render(request, 'controle/pages/criar_nova_missao.html', context)


class EditarMissaoView(UpdateView):
    model = Missao
    form_class = MissaoFormulario
    template_name = "controle/pages/criar_nova_missao.html"
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:principal')


# def deletar_missao(request, id):
#     missao = Missao.objects.get(pk=id)
#     if request.method == 'POST':
#         missao.delete()
#         return redirect('rpa_manager:principal')
#     return render(request, 'controle/pages/delete_mission.html', {'obj': missao})

class EventoDeleteView(DeleteView):
    model = Missao
    template_name = "controle/pages/delete_mission.html"
    context_object_name = 'form'
    success_url = reverse_lazy('rpa_manager:principal')