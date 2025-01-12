function Timeseries(dataJson) {
    
    console.log(dataJson.id) // id del dataset al que pertenece
    console.log(dataJson.type) 
    console.log(dataJson.unit)
    console.log(dataJson.name)
    console.log(dataJson.widgetid)

    widget_id = dataJson.widgetid

    //IMPORTANTE
    
    

    //preprocessiong logic


    var newSelectHtml = `
                <label for="colorInput" class="form-label mt-4">Choose a color</label>
                <input type="color" class="form-control form-control-color" id="colorInput" value="#563d7c" title="Choose a colorr"></input>
            `;
    $('#added-options').append(newSelectHtml);

    dataJson.color = "#563d7c"

    $('#colorInput').change(function() {
        dataJson.color = $(this).val();
    });
    
    
    if(1 == 1){

    }
    
    //preprocessiong logic
    
    final_json = dataJson;
    final_json.plot = "timeseries";
    final_json.generate = 'GenerateTimeseries';
    active_json = final_json;
    //$('#json-' + widget_id ).val(JSON.stringify(final_json));
    
    ActivarGuardar();
}


function RenderSeries(containerId, data) {
    const container = $(`#${containerId}`);

    // Set container dimensions to 95%
    container.css({
        margin: "auto"
    });

    // Create canvas element
    const canvasId = `${containerId}-chart`;
    //container.empty(); // Clear previous content
    container.append(`<canvas id="${canvasId}"></canvas>`);

    // Get canvas context
    const ctx = document.getElementById(canvasId).getContext("2d");

    // Calculate min and max for the y-axis
    const minValue = Math.min(...data.values);
    const maxValue = Math.max(...data.values);
    const padding = (maxValue - minValue) * 0.1; // Add 10% padding for better visualization

    // Create the chart
    new Chart(ctx, {
        type: "line",
        data: {
            labels: Array.from({ length: data.values.length }, (_, i) => i + 1), // Use indices as labels
            datasets: [{
                label: data.name,
                data: data.values,
                borderColor: data.color,
                backgroundColor: data.color,
                borderWidth: 2,
                tension: 0.4,
                pointRadius: 0 
            }]
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
                    title: {
                        display: false,
                        text: "Index"
                    }
                },
                y: {
                    title: {
                        display: false,
                        text: "Values"
                    },
                    suggestedMin: minValue - padding, // Adjust the minimum value
                    suggestedMax: maxValue + padding, // Adjust the maximum value
                    beginAtZero: false // Disable forcing zero as the minimum
                }
            }
        }
    });
}


function GenerateTimeseries(id, json) {
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(json),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            $('#placeholder-' + id).remove();
            RenderSeries("widget-body-" + id, response); // Solo pasa la respuesta directamente
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
