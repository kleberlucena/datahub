$(document).ready(function() {
    $('#table_missoes').DataTable( {
        responsive: true,
        "order": [[ 2, "desc" ]],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });

    $('#table_checklists').DataTable( {
        responsive: true,
        "order": [[ 3, "desc" ]],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });
    
    $('#table_efeitvo').DataTable( {
        responsive: true,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    } );

    $('#table_relatorios').DataTable( {
        responsive: true,
        "order": [[ 1, "desc" ]],
        "paging": true,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    } );

    $('#table_aeronaves').DataTable( {
        responsive: true,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });

    $('#table_baterias').DataTable( {
        responsive: true,
        "order": [[ 1, "desc" ]],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    } );

    // config para formulário do relatório
    $('.piloto_observador_escolha').select2();
    $('.local_escolha').select2();
    $('.opm_apoiada_escolha').select2();
    $('.unidade_apoiada_escolha').select2();
    $('.natureza_de_voo_escolha').select2();
    $('.aeronave_escolha').select2();
    
    // config para formulário do checklist
    $('.checklist_aeronave_escolha').select2();
} );