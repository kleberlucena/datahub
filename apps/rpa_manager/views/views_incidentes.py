from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from apps.rpa_manager.models import Incidentes, ImagensIncidente
from apps.rpa_manager.forms import IncidentesForm
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from apps.rpa_manager.handlers import require_permission
from django.contrib import messages

MESSAGE_MODEL_NAME = 'Incidente'


class IncidentesDetailView(PermissionRequiredMixin, DetailView):
    model = Incidentes
    template_name = 'rpa_manager/detail_incident.html'
    permission_required = 'rpa_manager.view_incidentes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        incidente = self.get_object()

        images = ImagensIncidente.objects.filter(incidente=incidente)
        
        image_urls = [image.imageIncidente.url for image in images]
        context['image_urls'] = image_urls
        
        return context
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class IncidentesCreateView(PermissionRequiredMixin, CreateView):
    model = Incidentes
    form_class = IncidentesForm
    template_name = 'rpa_manager/create_incident.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    permission_required = 'rpa_manager.add_incidente'
    
    def get_initial(self):
        return {
            'piloto': self.request.user
        }
     
    def get_form_kwargs(self):
        """
           o metodo abaixo busca o usuario logado para passar para
           uma query no forms desse model e pegar apenas objetos que
           o usuario logado criou
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        images = self.request.FILES.getlist('imagens')
        self.object = form.save()
        for image in images:
           ImagensIncidente.objects.create(incidente=self.object, imageIncidente=image)

        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criado com sucesso!')
        
        return redirect(self.get_success_url())
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class IncidentesUpdateView(PermissionRequiredMixin, UpdateView):
    model = Incidentes
    form_class = IncidentesForm
    template_name = 'rpa_manager/create_incident.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    permission_required = 'rpa_manager.change_incidente'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        images = self.request.FILES.getlist('imagens')
        
        self.object = form.save()

        for image in images:
            ImagensIncidente.objects.create(incidente=self.object, imageIncidente=image)

        messages.success(self.request, f'{MESSAGE_MODEL_NAME} editado com sucesso!')
        
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        incidente = self.get_object()

        images = ImagensIncidente.objects.filter(incidente=incidente)
        
        image_urls = [image.imageIncidente.url for image in images]
        context['image_urls'] = image_urls
        context['images'] = images
        
        return context
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class IncidentesDeleteView(PermissionRequiredMixin, DeleteView):
    model = Incidentes
    template_name = 'rpa_manager/delete_incident.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    permission_required = 'rpa_manager.delete_incidente'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} excluído com sucesso!')
        return response
    
    @method_decorator(require_permission(permission_required))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    
class IncidenteImageDeleteView(DeleteView):
    model = ImagensIncidente
    template_name = 'rpa_manager/delete_image.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    
    def delete(self, request, *args, **kwargs):
        imagem = self.get_object()
        if imagem:
            imagem.delete()
            return JsonResponse({'message': 'Imagem excluída com sucesso.'})
        else:
            return JsonResponse({'error': 'Imagem não encontrada.'}, status=404)
    
