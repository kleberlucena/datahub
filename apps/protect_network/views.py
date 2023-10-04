from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import  render, redirect, get_object_or_404
from django.utils import timezone
from . import models, forms
import json



class IndexView(TemplateView):
    template_name = 'protect_network/index.html'

class EstablishmentView(TemplateView):
    template_name = 'protect_network/establishment.html'

    def get(self, request, *args, **kwargs):
        form = forms.EstablishmentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.EstablishmentForm(request.POST)
        if form.is_valid():
            # Faça algo com os dados do formulário, se necessário
            return redirect('sucesso')  # Redirecione para a página de sucesso após o envio bem-sucedido

        return render(request, self.template_name, {'form': form})
    

class EmployeeView(TemplateView):
    template_name = 'protect_network/employee.html'

    def get(self, request, *args, **kwargs):
        form = forms.EmployeeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.EmployeeForm(request.POST)
        return render(request, self.template_name, {'form': form})


class WorkingHoursView(TemplateView):
    template_name = 'protect_network/working_hours.html'


class SecurityView(TemplateView):
    template_name = 'protect_network/security.html'

    def get(self, request, *args, **kwargs):
        form = forms.SecurityForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.SecurityForm(request.POST)
        return render(request, self.template_name, {'form': form})