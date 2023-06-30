from . views_funcoes_auxiliares import (obtem_localidade_com_maior_apoio,
                                       obtem_total_de_missoes,
                                       obtem_total_de_opms_apioadas,
                                       obtem_total_de_unidades_apioadas)

numero_de_missoes = obtem_total_de_missoes()
valor_opm_maior_apoio, nome_opm_maior_apoio = obtem_total_de_opms_apioadas()
valor_unidade_maior_apoio, nome_unidade_maior_apoio = obtem_total_de_unidades_apioadas()
nome_local, valor_local = obtem_localidade_com_maior_apoio()

dashboard_cards = [
    {   'title': 'Total de missões',
        'valor': numero_de_missoes,
        'url_do_icone': "/static/controle/img/medal.svg",
        'type': "simples",
        'color': 'dash_first_color'
    },
    {   'title': 'OPM que teve maior apoio',
        'valor': valor_opm_maior_apoio,
        'parametro': nome_opm_maior_apoio,
        'url_do_icone': "/static/controle/img/police-station.svg",
        'type': "completo",
        'color': 'dash_second_color'
    },
    {   'title': 'Unidade que teve maior apoio',
        'valor': valor_unidade_maior_apoio,
        'parametro': nome_unidade_maior_apoio,
        'url_do_icone': "/static/controle/img/police-station2.png",
        'type': "completo",
        'color': 'dash_third_color'
    },
    {   'title': 'Localidade que teve maior apoio',
        'valor': valor_local,
        'parametro': nome_local,
        'url_do_icone': "/static/controle/img/local.svg",
        'type': "completo",
        'color': 'dash_fourth_color'
    },
]
