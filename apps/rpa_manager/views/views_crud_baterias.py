from django.shortcuts import redirect, render

from apps.rpa_manager.forms import BateriaForm
from apps.rpa_manager.models import Bateria


def ver_bateria(request, id):
    bateria = Bateria.objects.get(pk=id)
    
    return render(request, 'controle/pages/ver_bateria.html', {'bateria': bateria})


def criar_nova_bateria(request):
    
    bateria_form = BateriaForm(request.POST)
    
    if request.method == 'POST':
        bateria_form = BateriaForm(request.POST)
        if bateria_form.is_valid():
            bateria_form.save()
            return redirect('controle:baterias')
    else:
        bateria_form = BateriaForm()
    
    return render(request, 'controle/pages/criar_nova_bateria.html', {'bateria_form': bateria_form, 'is_app_page': True,})

def editar_bateria(request, id):
    bateria = Bateria.objects.get(pk=id)
    bateria_form = BateriaForm(instance=bateria)
    
    if request.method == 'POST':
        bateria_form =  BateriaForm(request.POST, instance=bateria)
        if bateria_form.is_valid():
            bateria_form.save()
            return redirect('controle:baterias')

    context = {'bateria_form': bateria_form}
    return render(request, 'controle/pages/criar_nova_bateria.html', context)

def deletar_bateria(request, id):
    bateria = Bateria.objects.get(pk=id)
    if request.method == 'POST':
        bateria.delete()
        return redirect('controle:baterias')
    return render(request, 'controle/pages/delete_bateria.html', {'obj': bateria})