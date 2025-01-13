function Averagecake(dataJson) {
    
    console.log(dataJson.id) // id del dataset al que pertenece
    console.log(dataJson.title) 
    console.log(dataJson.type) 
    console.log(dataJson.unit)
    console.log(dataJson.name)
    console.log(dataJson.widgetid)

    dataset_id = dataJson.id
    widget_id = dataJson.widgetid

    //IMPORTANTE
    
    var newSelectHtml = `
                <div class="mt-4 mb-4 temp-input">
                <label for="second-attribute" class="form-label">Tags</label>
                <select id="second-attribute" class="select2 " name="state" style="width: 100%" placeholder="Choose an attribute">
                    <option></option>
                </select>
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
            $select2.append($('<option></option>'));
            $.each(attributes, function(index, attribute) {
                if (attribute.type == 'nominal'){
                    $select2.append($('<option></option>')
                        .attr('value', JSON.stringify(attribute))
                        .text(`${attribute.name} (${attribute.type})`));
                }
            });
        }
    });

    var values = dataJson
    var tags = {}
    


    $('#second-attribute').change(function() {
        tags = JSON.parse($('#second-attribute').val());


        final_json = {
            id: dataset_id,
            values: values.name,
            tags: tags.name,
        };
    
        final_json.plot = "averagebar";
        final_json.generate = 'GenerateAveragecake';
    
    
        //final JSON requirements: .generate .plot 
        active_json = final_json;
        
        //alert(JSON.stringify(final_json));
        ActivarGuardar();

    });
    
}



function RenderAveragecake(containerId, data) {
    const container = $(`#${containerId}`);

    container.find('canvas').remove();
    // Configura las dimensiones del contenedor al 95%
    container.css({
        margin: 0
    });

    // Crear el elemento canvas
    const canvasId = `${containerId}-chart`;
    container.append(`<canvas id="${canvasId}"></canvas>`);

    // Obtener el contexto del canvas
    const ctx = document.getElementById(canvasId).getContext("2d");

    // Generar colores automáticamente
    const generateColors = (count) => {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const hue = (i * 360 / count) % 360; // Distribuye los colores uniformemente
            colors.push(`hsl(${hue}, 70%, 60%)`); // Colores en formato HSL
        }
        return colors;
    };

    const colors = generateColors(data.labels.length);

    // Crear la gráfica de pastel
    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: data.labels, // Utiliza las etiquetas del JSON
            datasets: [{
                label: data.name || "Distribución de valores", // Etiqueta opcional
                data: data.values, // Valores del JSON
                backgroundColor: colors, // Colores generados automáticamente
                borderColor: "#ffffff", // Color del borde
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "top"
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.raw;
                            const total = context.dataset.data.reduce((sum, val) => sum + val, 0);
                            const percentage = ((value / total) * 100).toFixed(2);
                            return `${context.label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}



function GenerateAveragecake(id, json) {
    //alert("dr")
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(json),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            $('#placeholder-' + id).remove();
            RenderAveragecake("widget-body-" + id, response); // Solo pasa la respuesta directamente
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
