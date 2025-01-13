function Gauge(dataJson) {
    
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

                <div class="mt-2 mb-2 temp-input">
                <label for="colorInput" class="form-label mt-4">Choose a color</label>
                <input type="color" class="form-control form-control-color" id="colorInput" value="#563d7c" title="Choose a color" style="width: 100%"></input>
                </div>

                <div class=" mb-2 temp-input">
                <label for="min-gauge" class="form-label mt-4">Min value</label>
                <input type="text" class="form-control form-control-color" id="min-gauge" style="width: 100%"></input>
                </div>

                <div class=" mb-2 temp-input">
                <label for="max-gauge" class="form-label mt-4">Max value</label>
                <input type="text" class="form-control form-control-color" id="max-gauge" style="width: 100%"></input>
                </div>

                

                `;

    $('#added-options').append(newSelectHtml);
    //addedSelect();
    let color = "";
    $('#colorInput').change(function() {
        color = $(this).val();
    });


    let max_value;
    let min_value;
    $('#min-gauge').change(function() {
        min_value = parseFloat($('#min-gauge').val());
    });

    $('#max-gauge').change(function() {
        max_value = parseFloat($('#max-gauge').val());

        final_json = {
            id: dataset_id,
            color: color,
            column: dataJson.name,
            min_value: min_value,
            max_value: max_value,
        };
    
        final_json.plot = "gauge";
        final_json.generate = 'GenerateGauge';
    
    
        //final JSON requirements: .generate .plot 
        active_json = final_json;
        
        //alert(JSON.stringify(final_json));
        ActivarGuardar();

    });
    
}



function RenderGauge(containerId, data) {
    const container = $(`#${containerId}`);

    container.find('canvas').remove();

    // Configura las dimensiones del contenedor
    container.css({
        margin: 0
    });

    // Crea el elemento canvas
    const canvasId = `${containerId}-meter-chart`;
    container.append(`<canvas id="${canvasId}"></canvas>`);

    // Obtén el contexto del canvas
    const ctx = document.getElementById(canvasId).getContext("2d");

    // Calcula el tamaño de las partes del gráfico
    const totalRange = data.max_value - data.min_value;
    const readingValue = Math.max(Math.min(data.reading, data.max_value), data.min_value); // Asegúrate de que el reading esté dentro del rango
    const remainingValue = totalRange - (readingValue - data.min_value);



    // Genera el gráfico
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Medidor"],
            datasets: [
                {
                    label: readingValue,
                    data: [readingValue - data.min_value], // La parte verde
                    backgroundColor: data.color
                },
                {
                    label: "",
                    data: [remainingValue], // La parte gris
                    backgroundColor: "#f2f2f2"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: "top"
                }
            },
            scales: {
                x: {
                    stacked: true,
                    display: false // Oculta los ejes y el grid en el eje X
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    suggestedMin: data.min_value,
                    suggestedMax: data.max_value,
                    display: false // Oculta los ejes y el grid en el eje Y
                }
            }
        }
    });
}






function GenerateGauge(id, json) {
    //alert("dr")
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(json),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            $('#placeholder-' + id).remove();
            RenderGauge("widget-body-" + id, response); // Solo pasa la respuesta directamente
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
