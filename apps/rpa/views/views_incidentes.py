from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from apps.rpa.models import *
from apps.rpa.forms import *
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from apps.rpa.handlers import require_permission
from django.contrib import messages
from base.mixins import GroupRequiredMixin
from django.utils import timezone
from django.http import HttpResponseRedirect


MESSAGE_MODEL_NAME = 'Incidente'


class IncidentesDetailView(GroupRequiredMixin, DetailView):
    model = Incidents
    template_name = 'rpa/detail_incident.html'
    permission_required = 'rpa.view_incidentes'
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        incident = self.get_object()

        images = IncidentImage.objects.filter(incident=incident)
        
        image_urls = [image.imageIncident.url for image in images]
        context['image_urls'] = image_urls
        
        return context
    
    
class IncidentesCreateView(GroupRequiredMixin, CreateView):
    model = Incidents
    form_class = IncidentsForm
    template_name = 'rpa/create_incident.html'
    success_url = reverse_lazy('rpa:incidentes')
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_initial(self):
        return {
            'remote_pilot': self.request.user
        }
     
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        images = self.request.FILES.getlist('imagens')
        self.object = form.save()
        for image in images:
           IncidentImage.objects.create(incident=self.object, imageIncident=image)

        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criado com sucesso!')
        
        return redirect(self.get_success_url())
    
    
class IncidentesUpdateView(GroupRequiredMixin, UpdateView):
    model = Incidents
    form_class = IncidentsForm
    template_name = 'rpa/create_incident.html'
    success_url = reverse_lazy('rpa:incidentes')
    group_required = ['profile:rpa_advanced']
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        images = self.request.FILES.getlist('imagens')
        self.object = form.save()
        for image in images:
            IncidentImage.objects.create(incident=self.object, imageIncident=image)

        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editado com sucesso!')
        
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        incident = self.get_object()
        images = IncidentImage.objects.filter(incident=incident)
        
        image_urls = [image.imageIncident.url for image in images]
        context['image_urls'] = image_urls
        context['images'] = images
        
        return context
    
class IncidentesDeleteView(GroupRequiredMixin, DeleteView):
    model = Incidents
    template_name = 'rpa/delete_incident.html'
    success_url = reverse_lazy('rpa:incidentes')
    group_required = ['profile:rpa_advanced']

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluído com sucesso!')
        return response

class IncidenteImageDeleteView(DeleteView):
    model = IncidentImage
    template_name = 'rpa/delete_image.html'
    success_url = reverse_lazy('rpa:incidentes')
    
    def delete(self, request, *args, **kwargs):
        imagem = self.get_object()
        if imagem:
            imagem.delete()
            return JsonResponse({'message': 'Imagem excluída com sucesso.'})
        else:
            return JsonResponse({'error': 'Imagem não encontrada.'}, status=404)
    
