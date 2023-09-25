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
    

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import EmployeeForm, EmployeeFormSet

class EmployeeView(TemplateView):
    template_name = 'protect_network/employee.html'

    def get(self, request, *args, **kwargs):
        form = EmployeeForm()
        formset = EmployeeFormSet(prefix='employee')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = EmployeeForm(request.POST)
        formset = EmployeeFormSet(request.POST, request.FILES, prefix='employee')
        
        if form.is_valid() and formset.is_valid():
            # Processar os dados do formulário aqui (como salvar em um banco de dados, se necessário)
            # Lembre-se de que você pode acessar os dados do formulário e do formset usando form.cleaned_data e formset.cleaned_data
            
            # Por exemplo, você pode iterar sobre os formulários no formset assim:
            for form in formset:
                if form.cleaned_data:
                    print(form.cleaned_data)
            
            # Redirecionar ou fazer qualquer outra ação após o processamento dos dados
            return redirect('sucesso')  # Redirecione para a página de sucesso após o envio bem-sucedido

        return render(request, self.template_name, {'form': form, 'formset': formset})
