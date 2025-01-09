$(document).ready(function() {
    $('#data-select').change(function() {
        // Obtener el valor seleccionado
        var selectedOption = $(this).val();

        // Parsear el JSON del valor seleccionado
        var parsedOption = JSON.parse(selectedOption);
        

        // Verificar el tipo y mostrar la alerta correspondiente
        if (parsedOption.type === "escalar") {
            alert("delgado");
            $('#added-options').remove();
            var newSelectHtml = `
                <div id="added-options" class="mb-4">
                <label for="chart-type-select" class="form-label">Type of Chart</label>
                <select id="chart-type-select" class="select-plot" name="chartType" style="width: 100%">
                    <option value="bar">Barras</option>
                    <option value="scatter">Scatterplot</option>
                    <option value="max">Mostrar el máximo</option>
                </select>
                </div>
            `;
            $('#config-form').append(newSelectHtml);

        } else if (parsedOption.type === "intervalo") {
            alert("gordo");
            $('#added-options').remove();
            var newSelectHtml = `
                <div id="added-options" class="mb-4">
                <label for="chart-type-select" class="form-label">Type of Chart</label>
                <select id="chart-type-select" class="select-plot" name="chartType" style="width: 100%">
                    <option value="bar">Radar</option>
                    <option value="scatter">Direccion</option>
                    <option value="max">Mostrar el minimo</option>
                </select>
                </div>
            `;
            $('#config-form').append(newSelectHtml);


        } else if (parsedOption.type === "mapa") {
            alert("mapa");
        }
    });




    $(document).on('change', '#chart-type-select', function() {
        
        var selectedChartType = $(this).val();
    
        switch (selectedChartType) {
            case 'bar':
                BarChart();
                break;
            case 'scatter':
                var parsedOption = JSON.parse($('#data-select').val());
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