from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from apps.rpa_manager.models import *
from apps.rpa_manager.forms import *
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission
from django.contrib import messages
from base.mixins import GroupRequiredMixin
from django.utils import timezone
from django.http import HttpResponseRedirect


MESSAGE_MODEL_NAME = 'Incidente'


class IncidentesDetailView(GroupRequiredMixin, DetailView):
    model = Incidents
    template_name = 'rpa_manager/detail_incident.html'
    permission_required = 'rpa_manager.view_incidentes'
    group_required = ['profile:rpa_basic', 'profile:rpa_advanced']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        incident = self.get_object()

        images = IncidentImage.objects.filter(incident=incident)
        
        image_urls = [image.imageIncident.url for image in images]
        context['image_urls'] = image_urls
        
        return context
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class IncidentesCreateView(GroupRequiredMixin, CreateView):
    model = Incidents
    form_class = IncidentsForm
    template_name = 'rpa_manager/create_incident.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
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
    template_name = 'rpa_manager/create_incident.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
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
    
    def dispatch(self, *args, **kwargs):
        incidente = self.get_object()
        time_since_creation = timezone.now() - incidente.date
        if time_since_creation.total_seconds() > 24 * 60 * 60:  # 24 horas em segundos
            messages.error(self.request, 'Não é possível editar este incidente após 24 horas.')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(*args, **kwargs)
    
    
class IncidentesDeleteView(PermissionRequiredMixin, DeleteView):
    model = Incidents
    template_name = 'rpa_manager/delete_incident.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    permission_required = 'rpa_manager.delete_incidente'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.info(self.request, f'{MESSAGE_MODEL_NAME} excluído com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class IncidenteImageDeleteView(DeleteView):
    model = IncidentImage
    template_name = 'rpa_manager/delete_image.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    
    def delete(self, request, *args, **kwargs):
        imagem = self.get_object()
        if imagem:
            imagem.delete()
            return JsonResponse({'message': 'Imagem excluída com sucesso.'})
        else:
            return JsonResponse({'error': 'Imagem não encontrada.'}, status=404)
    
