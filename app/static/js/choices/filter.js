$(document).ready(function() {
    $('#data-select').change(function() {
        // Obtener el valor seleccionado
        var selectedOption = $(this).val();

        // Parsear el JSON del valor seleccionado
        var parsedOption = JSON.parse(selectedOption);
        

        // Verificar el tipo y mostrar la alerta correspondiente
        if (parsedOption.type === "numeric") {
            //alert("delgado");
            $('#added-options').remove();
            var newSelectHtml = `
                <div id="added-options" class="mb-4">
                <label for="chart-type-select" class="form-label">Type of Chart</label>
                <select id="chart-type-select" class="select-plot" name="chartType" style="width: 100%">
                    <option value="statistics">Estadisticas</option>
                    <option value="scatter">Scatterplot</option>
                    <option value="box">Caja</option>
                </select>
                </div>
            `;
            $('#config-form').append(newSelectHtml);

        } else if (parsedOption.type === "nominal") {
            //alert("gordo");
            $('#added-options').remove();
            var newSelectHtml = `
                <div id="added-options" class="mb-4">
                <label for="chart-type-select" class="form-label">Type of Chart</label>
                <select id="chart-type-select" class="select-plot" name="chartType" style="width: 100%">
                    <option value="moda">Moda</option>
                    <option value="bar">Conteo de instancias</option>
                    <option value="pastel">Distribucion</option>
                </select>
                </div>
            `;
            $('#config-form').append(newSelectHtml);


        } else if (parsedOption.type === "mapa") {
            //alert("mapa");
        }
    });




    $(document).on('change', '#chart-type-select', function() {
        
        var selectedChartType = $(this).val();
        
        var parsedOption = JSON.parse($('#data-select').val());
        parsedOption.widgetid = active_id;
        
        switch (selectedChartType) {
            
            case 'bar':
                BarChart();
                break;
            case 'scatter':
                Timeseries(parsedOption);
                break;
            case 'max':
                MaxValue();
                break;
            default:
                alert('Seleccione un tipo de gráfica válido.');
        }
    });
    
    





});