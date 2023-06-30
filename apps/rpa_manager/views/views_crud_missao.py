from django.shortcuts import redirect, render
from django.conf import settings

from . views_send_email import send_html_email
from apps.rpa_manager.forms import MissaoFormulario
from apps.rpa_manager.models import Missao

def ver_missao(request, id):
    missao = Missao.objects.get(pk=id)
    
    return render(request, 'controle/pages/ver_missao.html', {'missao': missao})

def criar_nova_missao(request):
    missao_form = MissaoFormulario(initial={'usuario': request.user})
    
    subject = "Nova missão cadastrada."
    recipient_list = ['marcospaivajr7@gmail.com']
     
    # 'diogenes.sousa@apps.pm.pb.gov.br'
    if request.method == 'POST':
        missao_form = MissaoFormulario(request.POST, initial={'usuario': request.user})
        if missao_form.is_valid():
            missao_form.save()
            html_message = 'emails/nova_missao.html'
            context = {
                'titulo': request.POST['titulo'],
                'STATIC_URL': settings.STATIC_URL}
            
            # send_html_email(subject, html_message, context, recipient_list)
            return redirect('controle:principal')
    
    context = {'missao_form': missao_form}
    return render(request, 'controle/pages/criar_nova_missao.html', context)


def editar_missao(request, id):
    missao = Missao.objects.get(pk=id)
    missao_form = MissaoFormulario(instance=missao)
    
    if request.method == 'POST':
        missao_form =  MissaoFormulario(request.POST, instance=missao)
        if missao_form.is_valid():
            missao_form.save()
            return redirect('controle:principal')

    context = {'missao_form': missao_form}
    return render(request, 'controle/pages/criar_nova_missao.html', context)

def deletar_missao(request, id):
    missao = Missao.objects.get(pk=id)
    if request.method == 'POST':
        missao.delete()
        return redirect('controle:principal')
    return render(request, 'controle/pages/delete_mission.html', {'obj': missao})