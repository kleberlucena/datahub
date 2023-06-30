from django.shortcuts import redirect, render

from . views_send_email import send_html_email
from apps.rpa_manager.forms import RelatorioFormulario
from apps.rpa_manager.models import Missao, Relatorio


def ver_relatorio(request, id):
    relatorio = Relatorio.objects.get(pk=id)
    
    return render(request, 'controle/pages/ver_relatorio.html', {'relatorio': relatorio})


def criar_novo_relatorio(request, id):
    missao = Missao.objects.get(pk=id)
    
    subject = "Missão concluída."
    recipient_list = ['marcospaivajr7@gmail.com']
    
    dados_missao = {
        'titulo': missao.titulo,
        'militar': request.user,
        'piloto_observador': missao.piloto_observador,
        'data': missao.data,
        'local': missao.local,
        # 'relato_da_missao': 'Sem alteração',
        'aeronave': missao.aeronave
    }
    relatorio_form = RelatorioFormulario(request.POST, initial=dados_missao)
    
    missao.concluida = relatorio_form['status_missao'].value()
    missao.save()
    
    if request.method == 'POST':
        relatorio_form = RelatorioFormulario(request.POST, request.FILES, initial=dados_missao)
        if relatorio_form.is_valid():
            relatorio_form.save()
            
            html_message = 'emails/missao_encerrada.html'
            context = {'titulo': missao.titulo}
            # send_html_email(subject, html_message, context, recipient_list)
            return redirect('controle:relatorios')
    else:
        relatorio_form = RelatorioFormulario(initial=dados_missao)
    
    return render(request, 'controle/pages/criar_novo_relatorio.html', {'relatorio_form': relatorio_form, 'is_app_page': True,})

def editar_relatorio(request, id):
    relatorio = Relatorio.objects.get(pk=id)
    relatorio_form = RelatorioFormulario(instance=relatorio)
    
    if request.method == 'POST':
        relatorio_form =  RelatorioFormulario(request.POST, request.FILES, instance=relatorio)
        if relatorio_form.is_valid():
            relatorio_form.save()
            return redirect('controle:relatorios')

    context = {'relatorio_form': relatorio_form}
    return render(request, 'controle/pages/criar_novo_relatorio.html', context)

def deletar_relatorio(request, id):
    relatorio = Relatorio.objects.get(pk=id)
    if request.method == 'POST':
        relatorio.delete()
        return redirect('controle:relatorios')
    return render(request, 'controle/pages/delete_relatorio.html', {'obj': relatorio})