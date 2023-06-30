from django.shortcuts import redirect, render

from apps.rpa_manager.forms import MilitarForm
from apps.rpa_manager.models import Militar


def ver_efetivo(request, id):
    militar = Militar.objects.get(pk=id)
    
    return render(request, 'controle/pages/ver_efetivo.html', {'militar': militar})

def criar_novo_militar(request):    
    militar_form = MilitarForm()

    if request.method == 'POST':
        militar_form = MilitarForm(request.POST)
        if militar_form.is_valid():
            militar_form.save()
            return redirect('controle:efetivo')
        
    context = {
                'is_app_page': True, 
                'militar_form': militar_form
            }
    return render(request, 'controle/pages/criar_novo_militar.html', context)


def editar_efetivo(request, id):
    militar = Militar.objects.get(pk=id)
    militar_form = MilitarForm(instance=militar)
    
    if request.method == 'POST':
        militar_form =  MilitarForm(request.POST, instance=militar)
        if militar_form.is_valid():
            militar_form.save()
            return redirect('controle:efetivo')

    context = {'militar_form': militar_form}
    return render(request, 'controle/pages/criar_novo_militar.html', context)


def deletar_efetivo(request, id):
    militar = Militar.objects.get(pk=id)
    if request.method == 'POST':
        militar.delete()
        return redirect('controle:efetivo')
    return render(request, 'controle/pages/delete_efetivo.html', {'obj': militar})