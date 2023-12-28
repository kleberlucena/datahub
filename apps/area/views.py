from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import  get_object_or_404
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Avg
from django.http import JsonResponse
from base.mixins import GroupRequiredMixin

from base.decorations.toast_decorator import include_toast
from apps.portal import models as portal_models
from . import models, forms


class AreaListView(ListView):
    model = models.Area
    template_name = 'area/areas.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AreaListView, self).get_context_data(**kwargs)
        area = models.Area.objects.all()
        context['areas'] = area
        return context
    

@include_toast
class CreateAreaView(CreateView):
    model = models.Area
    form_class = forms.AreaForm
    template_name = 'area/area_form.html'
    success_url = reverse_lazy('area:area_list')


@include_toast
class UpdateAreaView(UpdateView):
    model = models.Area
    template_name = 'area/area_form.html'
    form_class = forms.AreaForm
    success_url = reverse_lazy('area:area_list')


@include_toast
class DeleteAreaView(DeleteView):
    model = models.Area
    template_name = 'area/area_delete.html'
    success_url = reverse_lazy('area:area_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_to_delete'] = self.get_object()
        return context