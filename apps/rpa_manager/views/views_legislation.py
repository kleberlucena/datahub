from apps.rpa_manager.models import Legislation
from apps.rpa_manager.forms import LegislationForm
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

MESSAGE_MODEL_NAME = 'Legislação'


# class LegislationDetailView(GroupRequiredMixin, DetailView):
#     model = Legislation
#     template_name = 'rpa_manager/detail_aircraft.html'
#     context_object_name = 'aeronave'
#     pk_url_kwarg = 'pk'
#     group_required = ['profile:rpa_advanced']
    

class LegislationCreateView(CreateView):
    model = Legislation
    form_class = LegislationForm
    template_name = 'rpa_manager/create_legislation.html'
    success_url = reverse_lazy('rpa_manager:legislations')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'{MESSAGE_MODEL_NAME} criada com sucesso!')
        return response

    
# class EditarAeronaveView(GroupRequiredMixin, UpdateView):
#     model = Aeronave
#     form_class = AeronavesForm
#     template_name = 'rpa_manager/update_aircraft.html'
#     context_object_name = 'form'
#     pk_url_kwarg = 'pk'
#     success_url = reverse_lazy('rpa_manager:aeronaves')
#     group_required = ['profile:rpa_advanced']

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, f'{MESSAGE_MODEL_NAME} editada com sucesso!')
#         return response
    
    
# class DeletarAeronaveView(PermissionRequiredMixin, DeleteView):
#     model = Aeronave
#     template_name = 'rpa_manager/delete_aircraft.html'
#     context_object_name = 'obj'
#     pk_url_kwarg = 'pk'
#     success_url = reverse_lazy('rpa_manager:aeronaves')
#     permission_required = 'rpa_manager.delete_aeronave'
    
#     def delete(self, request, *args, **kwargs):
#         response = super().delete(request, *args, **kwargs)
#         messages.success(self.request, f'{MESSAGE_MODEL_NAME} excluída com sucesso!')
#         return response
    
#     @method_decorator(require_permission(permission_required))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


