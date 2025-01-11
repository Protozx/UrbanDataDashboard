function Timeseries(dataJson) {
    
    console.log(dataJson.id) //primarykey
    console.log(dataJson.type) 
    console.log(dataJson.unit)
    console.log(dataJson.name)
    

    //preprocessiong logic

    if(1 == 1){

    }

    //preprocessiong logic
    
    active_json =  dataJson;
    active_generate = GenerateSeries;
    ActivarGuardar();
}


function RenderSeries(containerId, fakeData, name) {
    const container = $(`#${containerId}`);
    
    // Set container dimensions to 95%
    container.css({
        margin: "auto" // Optional: center the container
    });

    // Create canvas element
    const canvasId = `${containerId}-chart`;
    //container.empty(); // Clear previous content
    container.append(`<canvas id="${canvasId}"></canvas>`);

    // Get canvas context
    const ctx = document.getElementById(canvasId).getContext("2d");

    // Create the chart
    new Chart(ctx, {
        type: "line",
        data: {
            labels: fakeData.labels,
            datasets: [{
                label: name,
                data: fakeData.values,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                borderWidth: 2,
                tension: 0.4, // Smooth lines
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
                        display: true,
                        text: "Months"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Values"
                    },
                    beginAtZero: true
                }
            }
        }
    });
}





function GenerateSeries(id, json){
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(json),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            //alert('Respuesta: ' + response);
            $('#placeholder-' + active_id).remove();
            RenderSeries("widget-body-" + active_id, response, json.name);
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
