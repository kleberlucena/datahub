from django.shortcuts import redirect, render
from apps.rpa.forms import *
from apps.rpa.models import *


def formulario_missao(request):
    form = OperationForm(initial={'user': request.user})
    
    if request.method == 'POST':
        form = OperationForm(request.POST, initial={'usuario': request.user})
        if form.is_valid():
            form.save()
            return redirect('controle:principal')
    
    context = {'form': form}
    return render(request, 'rpa/create_operation.html', context)


def baterias_em_nivel_critico(limite_de_ciclos):
    baterias_nivel_critico = Battery.objects.all().filter(num_cicles__gt=limite_de_ciclos)
    ids_baterias_nivel_critico = []

    for obj in baterias_nivel_critico:
        ids_baterias_nivel_critico.append(obj.id)

    return ids_baterias_nivel_critico
