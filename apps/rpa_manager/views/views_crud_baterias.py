from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rpa_manager.forms import BateriaForm
from apps.rpa_manager.models import Bateria
from django.views import View
from django.shortcuts import render, redirect

class VerBateriaView(DetailView):
    model = Bateria
    template_name = 'controle/pages/ver_bateria.html'
    context_object_name = 'bateria'
    pk_url_kwarg = 'pk'


class CriarNovaBateriaView(CreateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'controle/pages/criar_nova_bateria.html'
    success_url = reverse_lazy('rpa_manager:baterias')
    

class EditarBateriaView(UpdateView):
    model = Bateria
    form_class = BateriaForm
    template_name = 'controle/pages/editar_bateria.html'
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:baterias')


class DeletarBateriaView(DeleteView):
    model = Bateria
    template_name = 'controle/pages/delete_bateria.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('rpa_manager:baterias')
    
    
class UpdateAllBateriasView(View):
    template_name = 'controle/pages/update_all_batteries.html'

    def get(self, request):
        baterias = Bateria.objects.all()
        return render(request, self.template_name, {'baterias': baterias})

    def post(self, request):
        for bateria_id, num_ciclos in request.POST.items():
            if bateria_id.isdigit():
                bateria = Bateria.objects.get(id=int(bateria_id))
                bateria.num_ciclos = int(num_ciclos)
                bateria.save()

        
        return redirect('rpa_manager:painel')
