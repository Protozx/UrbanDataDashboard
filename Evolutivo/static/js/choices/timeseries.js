function Timeseries(dataJson) {
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(dataJson),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            alert('Respuesta: ' + response);
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
