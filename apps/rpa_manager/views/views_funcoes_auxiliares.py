from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import redirect, render

from apps.rpa_manager.forms import MissaoFormulario
from apps.rpa_manager.models import Relatorio, CidadesPB, Bateria


def obtem_localidade_com_maior_apoio():
    locais = []
    locais_apoiados = Relatorio.objects.values('local').annotate(opms_count=Count('local'))
    for local in locais_apoiados:
        locais.append(list(local.values()))
    local_dict = dict(locais)
    
    if len(locais) == 0:
        return 'desconhecido', 0
    
    local_maior_apoio = max(local_dict, key=local_dict.get)
    nome_local = CidadesPB.objects.get(id=local_maior_apoio)
    
    return nome_local, local_dict[local_maior_apoio]

def obtem_total_de_opms_apioadas():
    opms = []
    opms_apoiadas = Relatorio.objects.values('opm_apoiada').annotate(opms_count=Count('opm_apoiada'))
    for opm in opms_apoiadas:
        opms.append(list(opm.values()))
    opm_dict = dict(opms)
    
    if len(opms) == 0:
        return 'desconhecido', 0
    
    opm_maior_apoio = max(opm_dict, key=opm_dict.get)
    nome_opm = OPM.objects.get(id=opm_maior_apoio)
    
    return nome_opm, opm_dict[opm_maior_apoio]

def obtem_total_de_unidades_apioadas():
    unidades = []
    unidades_apoiadas = Relatorio.objects.values('unidade_apoiada').annotate(unidades_count=Count('unidade_apoiada'))
    for unidade in unidades_apoiadas:
        unidades.append(list(unidade.values()))
    unidade_dict = dict(unidades)
    
    if len(unidades) == 0:
        return 'desconhecido', 0
    
    unidade_maior_apoio = max(unidade_dict, key=unidade_dict.get)
    nome_unidade = Unidades.objects.get(id=unidade_maior_apoio)
    
    return nome_unidade, unidade_dict[unidade_maior_apoio]

def obtem_total_de_missoes():
    numero_de_missoes = Relatorio.objects.all().count()
    return numero_de_missoes

def obtem_numero_de_missoes_por_mes():
    dicionario_de_missoes = {}
    
    missoes_por_mes = Relatorio.objects.annotate(month=TruncMonth('data')) \
    .values('month') \
    .annotate(total=Count('id')) \
    .order_by('month')

    for missao in missoes_por_mes:
        ano = missao['month'].strftime('%Y')
        mes = missao['month'].strftime('%b')
        total = missao['total']

        if ano not in dicionario_de_missoes:
            dicionario_de_missoes[ano] = {}
        
        dicionario_de_missoes[ano][mes] = total

    return dicionario_de_missoes


def formulario_missao(request):
    form = MissaoFormulario(initial={'usuario': request.user})
    
    if request.method == 'POST':
        form = MissaoFormulario(request.POST, initial={'usuario': request.user})
        if form.is_valid():
            form.save()
            return redirect('controle:principal')
    
    context = {'form': form}
    return render(request, 'rpa_manager/create_operation.html', context)


def numero_de_missoes_por_usuario():
    ids = []
    total_de_missoes_por_usuario = []
    id_mais_recent = User.objects.latest('id').id + 1

    for usuario in reversed(range(1, id_mais_recent)):
        users = User.objects.all().filter(pk=usuario)

        try:
            ids.append(users[0].id)
        except IndexError:
            print("Error")
            continue

        total_de_missoes_por_usuario.append(Relatorio.objects.all().filter(militar_id=usuario).count())
    
    idsUsuariosPorMissoes = dict(zip(ids, total_de_missoes_por_usuario))

        
    return idsUsuariosPorMissoes


def baterias_em_nivel_critico(limite_de_ciclos):
    baterias_nivel_critico = Bateria.objects.all().filter(num_ciclos__gt=limite_de_ciclos)
    ids_baterias_nivel_critico = []

    for obj in baterias_nivel_critico:
        ids_baterias_nivel_critico.append(obj.id)

    return ids_baterias_nivel_critico
