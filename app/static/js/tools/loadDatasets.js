$(document).ready(function() {
    // Cargar datasets cuando se carga la página
    $.ajax({
        url: '/get-datasets',
        method: 'GET',
        success: function(datasets) {
            //alert(JSON.stringify(datasets));
            var $select = $('#source-select');
            $select.empty(); // Limpiar opciones anteriores
            $.each(datasets, function(index, dataset) {
                $select.append($('<option></option>').attr('value', dataset.id).text(dataset.name));
            });
        }
    });

    // Evento de cambio para actualizar los atributos cuando se selecciona un dataset
    $('#source-select').change(function() {
        var datasetId = $(this).val();
        updateAttributes(datasetId);
        //alert('cambio')
    });
});

function updateAttributes(datasetId) {
    $.ajax({
        url: `/get-attributes/${datasetId}`,
        method: 'GET',
        success: function(attributes) {
            var $select = $('#data-select');
            $select.empty(); // Limpiar opciones anteriores
            $.each(attributes, function(index, attribute) {
                $select.append($('<option></option>')
                    .attr('value', JSON.stringify(attribute))
                    .text(`${attribute.name} (${attribute.type})`));
            });
        }
    });
}
