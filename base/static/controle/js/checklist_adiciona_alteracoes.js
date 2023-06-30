let checkboxes = document.querySelectorAll('.checklist_item');
let textAreaContent = document.querySelector("#id_alteracoes");
let listaDeAlteracoes = []


checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        if(!checkbox.checked) {
            listaDeAlteracoes.push(checkbox.previousElementSibling.textContent);
            adicionaTextoEmTextArea(listaDeAlteracoes);
        } else if(listaDeAlteracoes.includes(checkbox.previousElementSibling.textContent)) {
            let indice =  listaDeAlteracoes.indexOf(checkbox.previousElementSibling.textContent);
            listaDeAlteracoes.splice(indice, 1);
        }
    })
})

function adicionaTextoEmTextArea(vetor) {
    vetor.forEach(function(indice) {
        if(!textAreaContent.value.includes(indice)) {
            textAreaContent.value += indice + ':' + '\n';
        } 
    })
}

function limpaAlteracoes() {
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = true;
    })
    textAreaContent.value = '';
    listaDeAlteracoes = [];
}