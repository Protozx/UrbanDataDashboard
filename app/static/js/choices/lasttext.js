function Lasttext(dataJson) {
    
    console.log(dataJson.id) // id del dataset al que pertenece
    console.log(dataJson.title) 
    console.log(dataJson.type) 
    console.log(dataJson.unit)
    console.log(dataJson.name)
    console.log(dataJson.widgetid)

    dataset_id = dataJson.id
    widget_id = dataJson.widgetid  

    var newSelectHtml = `

                <div class="mt-2 mb-2 temp-input">
                <label for="colorInput" class="form-label mt-4">Choose a color</label>
                <input type="color" class="form-control form-control-color" id="colorInput" value="#5761EA" title="Choose a color" style="width: 100%"></input>
                </div>                

                `;

    $('#added-options').append(newSelectHtml);
    //addedSelect();

    final_json = {
        id: dataset_id,
        column: dataJson.name,
        color: "#5761EA"
    };

    $('#colorInput').change(function() {
        final_json.color = $(this).val();
    });
    
    final_json.plot = "lasttext";
    final_json.generate = 'GenerateLasttext';

    //final JSON requirements: .generate .plot 
    active_json = final_json;
    
    //alert(JSON.stringify(final_json));
    ActivarGuardar();
    
}



function RenderLasttext(containerId, data) {
    const container = $(`#${containerId}`);

    container.find('h3').remove();

    var newSelectHtml = `
                <svg class="widget-svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
                    <!-- Texto "Last" -->
                    <text x="50%" y="40%" text-anchor="middle" font-size="80%">
                        Last
                    </text>
                    <!-- Texto dinámico con color hexadecimal y negritas -->
                    <text x="50%" y="60%" text-anchor="middle" font-size="80%" font-weight="bold" fill="${data.color}">
                        ${data.reading}
                    </text>
                </svg>

            `;
    container.append(newSelectHtml);
    //$('.widget-text-medium').fitText(0.9);

}



function GenerateLasttext(id, json) {
    //alert("dr")
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(json),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            $('#placeholder-' + id).remove();
            RenderLasttext("widget-body-" + id, response); // Solo pasa la respuesta directamente
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
