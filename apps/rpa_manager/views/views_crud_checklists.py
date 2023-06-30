from django.shortcuts import redirect, render

from apps.rpa_manager.forms import ChecklistForm
from apps.rpa_manager.models import Checklist


def ver_checklist(request, id):
    checklist = Checklist.objects.get(pk=id)
    lista_de_alteracoes = checklist.alteracoes.split('\n')
    nova_lista_alteracoes = []
    for item in lista_de_alteracoes:
        print(lista_de_alteracoes)
        if len(lista_de_alteracoes) == 1 and lista_de_alteracoes[0] == '':
            nova_lista_alteracoes.append('Sem alterações')
        else:
            nova_lista_alteracoes.append(item + ' | ')

    print(nova_lista_alteracoes)
    return render(request, 'controle/pages/ver_checklist.html',
                  {'checklist': checklist, 'nova_lista_alteracoes': nova_lista_alteracoes})

#create checklist
def checklist_form(request):
    dados_checklist = {
        'piloto': request.user,
        # 'alteracoes': 'Sem alteração',
    }
    
    checklist_form = ChecklistForm(initial=dados_checklist)
    

    if request.method == 'POST':
        checklist_form = ChecklistForm(request.POST, initial=dados_checklist)
        if checklist_form.is_valid():
            checklist_form.save()
            return redirect('controle:checklists')
        
    context = {
                'is_app_page': True, 
                'checklist_form': checklist_form
            }
    return render(request, 'controle/pages/checklist_form.html', context)


def editar_checklist(request, id):
    checklist = Checklist.objects.get(pk=id)
    checklist_form = ChecklistForm(instance=checklist)
    
    if request.method == 'POST':
        checklist_form =  ChecklistForm(request.POST, instance=checklist)
        if checklist_form.is_valid():
            checklist_form.save()
            return redirect('controle:checklists')

    context = {'checklist_form': checklist_form,
               'edicao_checklist': 'True'}
    return render(request, 'controle/pages/checklist_form.html', context)


def deletar_checklist(request, id):
    checklist = Checklist.objects.get(pk=id)
    if request.method == 'POST':
        checklist.delete()
        return redirect('controle:checklists')
    return render(request, 'controle/pages/delete_checklist.html', {'obj': checklist})
