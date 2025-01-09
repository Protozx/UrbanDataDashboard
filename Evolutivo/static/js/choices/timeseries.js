function Timeseries(dataJson) {
    

    console.log(dataJson.id) //primarykey
    console.log(dataJson.type) 
    console.log(dataJson.unit)
    

    var idwidget = $('#current-id').val();

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







    const fakeData = {
        labels: ["January", "February", "March", "April", "May", "June"],
        values: [10, 20, 15, 25, 30, 45]
    };

    // Function to create and render the chart
    function renderChart(containerId) {
        const container = $(`#${containerId}`);
        
        // Create canvas element
        const canvasId = `${containerId}-chart`;
        container.empty(); // Clear previous content
        container.append(`<canvas id="${canvasId}"></canvas>`);

        // Get canvas context
        const ctx = document.getElementById(canvasId).getContext("2d");

        // Create the chart
        new Chart(ctx, {
            type: "line",
            data: {
                labels: fakeData.labels,
                datasets: [{
                    label: "Sample Data",
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

    $('#placeholder-' + idwidget).remove();
    renderChart("widget-body-" + idwidget);




    



}
