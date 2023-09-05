from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.portal.models import Entity, Military
from .models import AcceptTermsOfUseSASP
from .forms import AcceptTermsOfUseSASPForm


class TermsSASPView(TemplateView):
    template_name = 'termos-de-uso-sasp.html'


class TermsSASPCreateView(CreateView):
    model = AcceptTermsOfUseSASP
    template_name = 'termos-de-uso-sasp-form.html'
    form_class = AcceptTermsOfUseSASPForm
    success_url = reverse_lazy('https://sasp.apps.pm.pb.gov.br')

    def get_initial(self):
        # call super if needed
        user = self.request.user
        military = Military.objects.get(cpf=user.username)
        entity = Entity.objects.get(id=military.entity.id)
        return {'created_by': user, 'entity': entity,}
    

class TermsSASPListView(ListView):
    model = AcceptTermsOfUseSASP
    template_name = 'terms_sasp/terms_sasp_list.html'
    context_object_name = 'terms_sasp'

    
class TermsSASPDetailView(DetailView):
    model = AcceptTermsOfUseSASP
    template_name = 'terms_sasp/terms_sasp_detail.html'


class TermsSASPUpdateView(UpdateView):
    model = AcceptTermsOfUseSASP
    form_class = AcceptTermsOfUseSASPForm
    template_name = 'terms_sasp/terms_sasp_form.html'
    success_url = reverse_lazy('terms_sasp_list')


class TermsSASPDeleteView(DeleteView):
    model = AcceptTermsOfUseSASP
    template_name = 'terms_sasp/terms_sasp_confirm_delete.html'
    success_url = reverse_lazy('terms_sasp_list')