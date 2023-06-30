
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from apps.rpa_manager.models import Aeronave, Bateria, Checklist, Militar, Missao, Relatorio
from . views_cards import cards
from . views_crud_aeronaves import *
from . views_crud_baterias import *
from . views_crud_checklists import *
from . views_crud_efetivo import *
from . views_crud_missao import *
from . views_crud_relatorio import *
from . views_dashboard_cards import dashboard_cards
from . views_funcoes_auxiliares import *


def home(request):
    return render(request, 'controle/pages/base.html')


def painel(request):    
    context = {
        'cards' : cards
    }

    return render(request, 'controle/pages/painel.html', context)

def dashboard(request):
    numero_de_missoes = obtem_total_de_missoes()
    missoes_por_mes = obtem_numero_de_missoes_por_mes()
    opm_maior_apoio, numero_opm_maior_apoio = obtem_total_de_opms_apioadas()
    unidade_maior_apoio, numero_unidade_maior_apoio = obtem_total_de_unidades_apioadas()
    local_maior_apoio, numero_local_maior_apoio = obtem_localidade_com_maior_apoio()
    
    context = {
        'numero_de_missoes': numero_de_missoes,
        'missoes_por_mes': missoes_por_mes,
        'opm_maior_apoio': opm_maior_apoio,
        'numero_opm_maior_apoio': numero_opm_maior_apoio,
        'unidade_maior_apoio': unidade_maior_apoio,
        'numero_unidade_maior_apoio': numero_unidade_maior_apoio,
        'local_maior_apoio': local_maior_apoio,
        'numero_local_maior_apoio': numero_local_maior_apoio,
        'dashboard_cards' : dashboard_cards,
    }
    
    return render(request, 'controle/pages/dashboard.html', context)

def obtem_dados_de_missoes_por_mes(request):
    missoes_por_mes = obtem_numero_de_missoes_por_mes()
    
    return JsonResponse(missoes_por_mes, safe=False)

def obtem_dados_de_missoes_por_usuario(request):
    missoes_por_usuario = numero_de_missoes_por_usuario()
    usuariosPorMissoes = {}
    
    for usuario in missoes_por_usuario:
        new_key = str(User.objects.get(pk=usuario)) 
        value = missoes_por_usuario[usuario]
        usuariosPorMissoes[new_key] = value
        
    return JsonResponse(usuariosPorMissoes, safe=False)
    
def principal(request):
    missoes = Missao.objects.all().order_by('-data', '-horario')
    form = formulario_missao(request)
    
    context = { 'missoes': missoes,
                'is_app_page': True, 
                'form': form,
                'cards' : cards, 
                }
    
    return render(request, 'controle/pages/tela_principal.html', context)

def checklists(request):
    checklists = Checklist.objects.all().order_by('-data', '-horario')
    form = formulario_missao(request)
     
    context = { 
                'checklists': checklists, 
                'is_app_page': True, 
                'form': form,
                'cards': cards,
            }
    return render(request, 'controle/pages/checklists.html', context)


def relatorios(request):
    relatorios = Relatorio.objects.all().order_by('-horario_inicial', '-data')
    
    form = formulario_missao(request)

    context = {
                'relatorios': relatorios,

                'is_app_page': True, 
                'form': form,
                'cards': cards,
            }
    return render(request, 'controle/pages/relatorios.html', context)


def efetivo(request):
    militares = Militar.objects.all()
    numero_de_usuarios = User.objects.count()

    missoes_por_usuario = numero_de_missoes_por_usuario()
    
    form = formulario_missao(request)
      
    context = { 'militares': militares, 
                'is_app_page': True, 
                'form': form, 
                'missoes_por_usuario': missoes_por_usuario,
                'numero_de_usuarios': numero_de_usuarios,
                'cards': cards,
            }

    return render(request, 'controle/pages/usuarios.html', context)


def aeronaves(request):
    aeronaves = Aeronave.objects.all()

    form = formulario_missao(request)
    
    context= {
                'aeronaves': aeronaves, 
                'is_app_page': True, 
                'form': form,
                'cards': cards,
            }
    return render(request, 'controle/pages/aeronaves.html', context)


def baterias(request):
    limite_de_ciclos = 45 
    
    baterias = Bateria.objects.all()
    
    ids_baterias_nivel_critico = baterias_em_nivel_critico(limite_de_ciclos)

    form = formulario_missao(request)
 
    context = { 
                'baterias': baterias,
                'ids_baterias_nivel_critico': ids_baterias_nivel_critico, 
                'is_app_page': True, 
                'form': form,
                'cards': cards,
            }
    return render(request, 'controle/pages/baterias.html', context)

def retorna_total_de_missoes(request):
    total_de_missoes = Missao.objects.count()
    
    return JsonResponse({'total_de_missoes': total_de_missoes})
