let map;
let geocoder;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -23.550520, lng: -46.633308 }, // Coordenadas de São Paulo
        zoom: 8,
    });
    geocoder = new google.maps.Geocoder();
    document.getElementById("address").focus();

    const autocomplete = new google.maps.places.Autocomplete(document.getElementById("address"));
    autocomplete.bindTo("bounds", map);

    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }
        map.setCenter(place.geometry.location);
        map.setZoom(17); // Zoom mais próximo
        new google.maps.Marker({
            position: place.geometry.location,
            map: map
        });
        fillInAddress(place); // Função para preencher os campos
    });
}

function fillInAddress(place) { // Função para preencher os dados no formulário
    document.getElementById('latitude').value = place.geometry.location.lat();
    document.getElementById('longitude').value = place.geometry.location.lng();
    document.getElementById('formattedAddress').value = place.formatted_address;
}

function geocodeAddress(geocoder, resultsMap) {
    const address = document.getElementById("address").value;
    geocoder.geocode({ 'address': address }, function(results, status) {
        if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location
            });
            fillInAddress(results[0]);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

document.getElementById('saveLocationForm').onsubmit = function(event) {
    event.preventDefault(); // Evita o envio padrão do formulário
    // Aqui você pode fazer uma chamada AJAX para salvar os dados ou enviar o formulário normalmente.
    console.log('Latitude:', document.getElementById('latitude').value);
    console.log('Longitude:', document.getElementById('longitude').value);
    console.log('Endereço:', document.getElementById('formattedAddress').value);
    // Implementar chamada AJAX ou outra lógica de submissão
};

window.onload = initMap;
