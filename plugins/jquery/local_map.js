function initMap() {
    var input = document.getElementById('id_endereco');
    var autocomplete = new google.maps.places.Autocomplete(input);

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        document.getElementById('id_latitude').value = place.geometry.location.lat();
        document.getElementById('id_longitude').value = place.geometry.location.lng();
    });
}
