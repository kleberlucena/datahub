from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from apps.rpa_manager.models import Incidentes, ImagensIncidente
from apps.rpa_manager.forms import IncidentesForm
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class IncidentesCreateView(CreateView):
    model = Incidentes
    form_class = IncidentesForm
    template_name = 'controle/pages/create_incidente.html'
    success_url = reverse_lazy('rpa_manager:incidentes')

    
    def get_initial(self):
        return {
            'piloto': self.request.user
        }
    
    # o metodo abaixo buscar o usuario logado para passar para
    # uma query no forms desse model e pegar apenas objetos que
    # o usuario logado criou
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        images = self.request.FILES.getlist('imagens')
        self.object = form.save()
        for image in images:
           ImagensIncidente.objects.create(incidente=self.object, imageIncidente=image)

        return redirect(self.get_success_url())
    
    
class IncidentesUpdateView(PermissionRequiredMixin, UpdateView):
    model = Incidentes
    form_class = IncidentesForm
    template_name = 'controle/pages/create_incidente.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    permission_required = 'rpa_manager.edit_incidente'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        images = self.request.FILES.getlist('imagens')
        
        self.object = form.save()

        for image in images:
            ImagensIncidente.objects.create(incidente=self.object, imageIncidente=image)

        return redirect(self.get_success_url())

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        incidente = self.get_object()

        images = ImagensIncidente.objects.filter(incidente=incidente)
        
        image_urls = [image.imageIncidente.url for image in images]
        context['image_urls'] = image_urls
        context['images'] = images
        
        return context
    
    
class IncidentesDeleteView(PermissionRequiredMixin, DeleteView):
    model = Incidentes
    template_name = 'controle/pages/delete_incidente.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    permission_required = 'rpa_manager.delete_incidente'

class IncidentesDetailView(DetailView):
    model = Incidentes
    template_name = 'controle/pages/ver_incidente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        incidente = self.get_object()

        images = ImagensIncidente.objects.filter(incidente=incidente)
        
        image_urls = [image.imageIncidente.url for image in images]
        context['image_urls'] = image_urls
        
        return context
    
    
class IncidenteImageDeleteView(DeleteView):
    model = ImagensIncidente
    template_name = 'controle/pages/delete_image.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    
    def delete(self, request, *args, **kwargs):
        imagem = self.get_object()
        if imagem:
            imagem.delete()
            return JsonResponse({'message': 'Imagem excluída com sucesso.'})
        else:
            return JsonResponse({'error': 'Imagem não encontrada.'}, status=404)
    
