from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from apps.rpa_manager.models import Incidentes, ImagensIncidente
from apps.rpa_manager.forms import IncidentesForm
from django.urls import reverse


class IncidentesCreateView(CreateView):
    model = Incidentes
    form_class = IncidentesForm
    template_name = 'controle/pages/create_incidente.html'
    success_url = reverse_lazy('rpa_manager:incidentes')

    def form_valid(self, form):
        # Get the images from the form's input field
        images = self.request.FILES.getlist('imagens')
        
        # Save the incident first to get its primary key
        self.object = form.save()

        # Associate the images with the incident
        for image in images:
           ImagensIncidente.objects.create(incidente=self.object, imageIncidente=image)

        return redirect(self.get_success_url())
    
    
class IncidentesUpdateView(UpdateView):
    model = Incidentes
    form_class = IncidentesForm
    template_name = 'controle/pages/create_incidente.html'
    success_url = reverse_lazy('rpa_manager:incidentes')

    def form_valid(self, form):
        # Get the images from the form's input field
        images = self.request.FILES.getlist('imagens')
        
        # Save the incident first to get its primary key
        self.object = form.save()

        # Associate the images with the incident
        for image in images:
            ImagensIncidente.objects.create(incidente=self.object, imageIncidente=image)

        return redirect(self.get_success_url())

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the Incidentes instance
        incidente = self.get_object()

        # Get all related images for the incidente
        images = ImagensIncidente.objects.filter(incidente=incidente)
        
        # Extract the image URLs and include them in the context
        image_urls = [image.imageIncidente.url for image in images]
        context['image_urls'] = image_urls
        context['images'] = images
        
        return context
    
    
class IncidentesDeleteView(DeleteView):
    model = Incidentes
    template_name = 'controle/pages/delete_incidente.html'
    success_url = reverse_lazy('rpa_manager:incidentes')


class IncidentesDetailView(DetailView):
    model = Incidentes
    template_name = 'controle/pages/ver_incidente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the Incidentes instance
        incidente = self.get_object()

        # Get all related images for the incidente
        images = ImagensIncidente.objects.filter(incidente=incidente)
        
        
        # Extract the image URLs and include them in the context
        image_urls = [image.imageIncidente.url for image in images]
        context['image_urls'] = image_urls
        
        return context
    
    
class IncidenteImageDeleteView(DeleteView):
    model = ImagensIncidente
    template_name = 'controle/pages/delete_image.html'
    success_url = reverse_lazy('rpa_manager:incidentes')
    
    

    
