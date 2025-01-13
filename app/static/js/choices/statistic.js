function Statistic(dataJson) {
    //DesactivarGuardar();
    console.log(dataJson.id) // id del dataset al que pertenece
    console.log(dataJson.title) 
    console.log(dataJson.type) 
    console.log(dataJson.unit)
    console.log(dataJson.name)
    console.log(dataJson.widgetid)

    dataset_id = dataJson.id
    widget_id = dataJson.widgetid  

    var newSelectHtml = `

                <div class="mt-3 mb-3 temp-input">
                <label for="select-statistic" class="form-label">Choose the statistic</label>
                <select id="select-statistic" class="select2" name="state" style="width: 100%" placeholder="Choose an statistic">
                    <option value="Max">Max</option>
                    <option value="Min">Min</option>
                    <option value="Mean">Mean</option>
                    <option value="Median">Median</option>
                    <option value="Mode">Mode</option>
                    <option value="Variance">Variance</option>
                </select>
                </div>

                <div class="mb-2 temp-input">
                <label for="second-attribute" class="form-label">Get with</label>
                <select id="second-attribute" class="select2" name="state" style="width: 100%" placeholder="Choose an attribute">
                    <option value="None">None</option>
                </select>
                </div>
                
                <div class="mb-2 temp-input">
                <label for="colorInput" class="form-label mt-2">Choose a color</label>
                <input type="color" class="form-control form-control-color" id="colorInput" value="#5761EA" title="Choose a color" style="width: 100%"></input>
                </div>  

                `;

    $('#added-options').append(newSelectHtml);
    //addedSelect();

    $.ajax({
        url: `/get-attributes/${dataset_id}`,
        method: 'GET',
        success: function(attributes) {
            var $select2 = $('#second-attribute');
            $select2.empty(); // Limpiar opciones anteriores
            $select2.append($('<option value="none">None</option>'));
            $.each(attributes, function(index, attribute) {
                
                $select2.append($('<option></option>')
                    .attr('value', JSON.stringify(attribute))
                    .text(`${attribute.name} (${attribute.type})`));
                
            });
        }
    });

    final_json = {
        id: dataset_id,
        column_1: dataJson.name,
        color: "#5761EA"
    };

    $('#colorInput').change(function() {
        final_json.color = $(this).val();
    });

    $('#second-attribute').change(function() {
        let second = "None";

        alert($('#second-attribute').val())
        if($('#second-attribute').val() != "None"){
            second = JSON.parse($('#second-attribute').val()).name;
        }

        final_json.statistic = $('#select-statistic').val();
        final_json.column_2 = second;

        final_json.plot = "statistic";
        final_json.generate = 'GenerateStatistic';
    
    
        //final JSON requirements: .generate .plot 
        active_json = final_json;
        
        //alert(JSON.stringify(final_json));
        ActivarGuardar();

    });
    
}



function RenderStatistic1(containerId, data) {
    const container = $(`#${containerId}`);

    container.find('h3').remove();

    var newSelectHtml = `
                <svg class="widget-svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
                    <text x="20%" y="8%" text-anchor="middle" font-size="30%">
                        ${data.column_1}
                    </text>    
                    <!-- Texto "last" -->
                    <text x="50%" y="45%" text-anchor="middle" font-size="80%">
                        ${data.statistic}
                    </text>
                    <!-- Texto dinámico con color hexadecimal y negritas -->
                    <text x="50%" y="65%" text-anchor="middle" font-size="80%" font-weight="bold" fill="${data.color}">
                        ${data.value_1}
                    </text>
                </svg>

            `;
    container.append(newSelectHtml);
    //$('.widget-text-medium').fitText(0.9);

}

function RenderStatistic2(containerId, data) {
    const container = $(`#${containerId}`);

    container.find('h3').remove();

    var newSelectHtml = `
                <svg class="widget-svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
                    <text x="20%" y="8%" text-anchor="middle" font-size="30%">
                        ${data.column_1}
                    </text>    
                     <!-- Texto " last" -->
                    <text x="50%" y="25%" text-anchor="middle" font-size="80%">
                        ${data.statistic}
                    </text>
                    <!-- Texto dinámico con color hexadecimal y negritas -->
                    <text x="50%" y="45%" text-anchor="middle" font-size="90%" font-weight="bold" fill="${data.color}">
                        ${data.value_1}
                    </text>
                    <text x="50%" y="65%" text-anchor="middle" font-size="80%">
                        at
                    </text>
                    <!-- Texto dinámico con color hexadecimal y negritas -->
                    <text x="50%" y="85%" text-anchor="middle" font-size="80%" font-weight="bold" fill="${data.color}">
                        ${data.value_2}
                    </text>
                </svg>

            `;
    container.append(newSelectHtml);
    //$('.widget-text-medium').fitText(0.9);

}



function GenerateStatistic(id, json) {
    //alert("dr")
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(json),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            $('#placeholder-' + id).remove();
            alert(JSON.stringify(response));
            if (response.graph == 1) {
                RenderStatistic1("widget-body-" + id, response);
            } else {
                RenderStatistic2("widget-body-" + id, response);
            }

             // Solo pasa la respuesta directamente
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
