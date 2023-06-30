$(document).ready(function() {
    let edicao_checklist = document.querySelector('.edicao_checklist');
    let edicao_de_checklist = edicao_checklist.textContent === 'True';
    if(!edicao_de_checklist){
        $(".formulario_checklist_titulo_selecao").hide();
        $(".formulario_checklist_selecao_itens ").hide();
    };

    $(".aeronave_escolha").on('change', function() {
        $(".formulario_checklist_titulo_selecao").show();
        $(".formulario_checklist_selecao_itens ").show();

        // Caso a aeronave seja Enterprise mostra itens adicionais
        let aeronave_selecionada = $(this).val();
        console.log(aeronave_selecionada);
        if (aeronave_selecionada === '1') {
            console.log("Aeronave 68 selecionada");
            $('input[name="holofote"]').show();
            $('label[for="id_holofote"]').show();

            $('input[name="auto_falante"]').show();
            $('label[for="id_auto_falante"]').show();

            $('input[name="luz_estroboscopica"]').show();
            $('label[for="id_luz_estroboscopica"]').show();

            $('input[name="smart_controller"]').show();
            $('label[for="id_smart_controller"]').show();

            $('input[name="controle"]').hide();
            $('label[for="id_controle"]').hide();
        } else {
            $('input[name="holofote"]').hide();
            $('label[for="id_holofote"]').hide();

            $('input[name="auto_falante"]').hide();
            $('label[for="id_auto_falante"]').hide();

            $('input[name="luz_estroboscopica"]').hide();
            $('label[for="id_luz_estroboscopica"]').hide();

            $('input[name="smart_controller"]').hide();
            $('label[for="id_smart_controller"]').hide();

            $('input[name="controle"]').show();
            $('label[for="id_controle"]').show();
        }
    });
});