from django.shortcuts import redirect, render

from apps.rpa_manager.forms import AeronavesForm
from apps.rpa_manager.models import Aeronave 


def ver_aeronave(request, id):
    aeronave = Aeronave.objects.get(pk=id)
    
    return render(request, 'controle/pages/ver_aeronave.html', {'aeronave': aeronave})


def criar_nova_aeronave(request):
    
    aeronave_form = AeronavesForm(request.POST)
    
    if request.method == 'POST':
        aeronave_form = AeronavesForm(request.POST)
        if aeronave_form.is_valid():
            aeronave_form.save()
            return redirect('controle:aeronaves')
    else:
        aeronave_form = AeronavesForm()
    
    return render(request, 'controle/pages/criar_nova_aeronave.html', {'aeronave_form': aeronave_form, 'is_app_page': True,})

def editar_aeronave(request, id):
    aeronave = Aeronave.objects.get(pk=id)
    aeronave_form = AeronavesForm(instance=aeronave)
    
    if request.method == 'POST':
        aeronave_form =  AeronavesForm(request.POST, request.FILES, instance=aeronave)
        if aeronave_form.is_valid():
            aeronave_form.save()
            return redirect('controle:aeronaves')

    context = {'aeronave_form': aeronave_form}
    return render(request, 'controle/pages/criar_nova_aeronave.html', context)

def deletar_aeronave(request, id):
    aeronave = Aeronave.objects.get(pk=id)
    if request.method == 'POST':
        aeronave.delete()
        return redirect('controle:aeronaves')
    return render(request, 'controle/pages/delete_aeronave.html', {'obj': aeronave})