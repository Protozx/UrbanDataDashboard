$(document).ready(function() {

    $('.select-source').change(function() {
        DesactivarGuardar();
    })

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
                <select id="chart-type-select" class="select-plot select2" name="chartType" style="width: 100%">
                    <option></option>
                    <option value="timeseries">Timeseries</option>
                    <option value="averagebar">Average by label (bar)</option>
                    <option value="averagecake">Average by label (cake)</option>
                    <option value="gauge">Gauge</option>
                    <option value="heatmap">Heatmap</option>
                </select>
                </div>
            `;
            $('#config-form').append(newSelectHtml);
            addedSelect();

        } else if (parsedOption.type === "nominal") {
            //alert("gordo");
            $('#added-options').remove();
            var newSelectHtml = `
                <div id="added-options" class="mb-4">
                <label for="chart-type-select" class="form-label">Type of Chart</label>
                <select id="chart-type-select" class="select-plot select2" name="chartType" style="width: 100%">
                    <option></option>
                    <option value="lasttext">Last value</option>
                </select>
                </div>
            `;
            $('#config-form').append(newSelectHtml);
            addedSelect();


        } else if (parsedOption.type === "none") {
            //alert("mapa");
        }
    });




    $(document).on('change', '#chart-type-select', function() {
        
        var selectedChartType = $(this).val();
        
        var parsedOption = JSON.parse($('#data-select').val());
        parsedOption.widgetid = active_id;
        parsedOption.title = $('#widget-title');
        $('.temp-input').remove();

        switch (selectedChartType) {
            
            case 'heatmap':
                Heatmap(parsedOption);
                break;
            case 'timeseries':
                Timeseries(parsedOption);
                break;
            case 'gauge':
                Gauge(parsedOption);
                break;
            case 'averagebar':
                Averagebar(parsedOption);
                break;
            case 'averagecake':
                Averagecake(parsedOption);
                break;
            case 'lasttext':
                Lasttext(parsedOption);
                break;
            default:
                alert('Seleccione un tipo de gráfica válido.');
        }


        

    });
    
    





});