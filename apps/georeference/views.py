from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from base.mixins import GroupRequiredMixin
from base.decorations.toast_decorator import include_toast
from . import models, forms


class AreaListView(GroupRequiredMixin, ListView):
    model = models.Area
    template_name = 'georeference/areas.html'
    group_required = ['profile:georeference_basic', 'profile:georeference_advanced', 'profile:georeference_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(AreaListView, self).get_context_data(**kwargs)
        area = models.Area.objects.all()
        context['areas'] = area
        return context
    

@include_toast
class CreateAreaView(GroupRequiredMixin, CreateView):
    model = models.Area
    form_class = forms.AreaForm
    template_name = 'georeference/area_form.html'
    group_required = ['profile:georeference_advanced', 'profile:georeference_manager']
    success_url = reverse_lazy('georeference:area_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['function_type'] = 'create'
        return context


@include_toast
class UpdateAreaView(GroupRequiredMixin, UpdateView):
    model = models.Area
    template_name = 'georeference/area_form.html'
    group_required = ['profile:georeference_advanced', 'profile:georeference_manager']
    form_class = forms.AreaForm
    success_url = reverse_lazy('georeference:area_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['function_type'] = 'update'
        area = self.get_object()
        context['polygon_data'] = area.area_polygon.geojson if area.area_polygon else None

        return context
    
@include_toast
class DetailAreaView(GroupRequiredMixin, DetailView):
    model = models.Area
    template_name = 'georeference/area_detail.html'
    group_required = ['profile:georeference_basic','profile:georeference_advanced', 'profile:georeference_manager']
    form_class = forms.AreaForm
    success_url = reverse_lazy('georeference:area_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['function_type'] = 'detail'
        return context


@include_toast
class DeleteAreaView(GroupRequiredMixin, DeleteView):
    model = models.Area
    template_name = 'georeference/area_delete.html'
    group_required = ['profile:georeference_manager']
    success_url = reverse_lazy('georeference:area_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_to_delete'] = self.get_object()
        return context
    
    
class CategoryListView(GroupRequiredMixin, ListView):
    model = models.Category
    template_name = 'georeference/categories.html'
    group_required = ['profile:georeference_basic','profile:georeference_advanced', 'profile:georeference_manager']

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        category = models.Category.objects.all()
        context['categories'] = category
        return context
    

@include_toast
class CreateCategoryView(GroupRequiredMixin, CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'georeference/category_form.html'
    group_required = ['profile:georeference_manager']
    success_url = reverse_lazy('georeference:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['function_type'] = 'create'
        return context


@include_toast
class UpdateCategoryView(GroupRequiredMixin, UpdateView):
    model = models.Category
    template_name = 'georeference/category_form.html'
    group_required = ['profile:georeference_manager']
    form_class = forms.CategoryForm
    success_url = reverse_lazy('georeference:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['function_type'] = 'update'
        category = self.get_object()

        return context
    


@include_toast
class DeleteCategoryView(GroupRequiredMixin, DeleteView):
    model = models.Category
    template_name = 'georeference/category_delete.html'
    group_required = ['profile:georeference_manager']
    success_url = reverse_lazy('georeference:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_to_delete'] = self.get_object()
        return context