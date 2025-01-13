function Heatmap(dataJson) {
    
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
                <label for="second-attribute" class="form-label">Latitude</label>
                <select id="second-attribute" class="select2" name="state" style="width: 100%" placeholder="Choose an attribute">
                    <option></option>
                </select>
                </div>

                <div class="mb-4 temp-input">
                <label for="third-attribute" class="form-label">Longitude</label>
                <select id="third-attribute" class="select2" name="state" style="width: 100%" placeholder="Choose an attribute">
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
            var $select3 = $('#third-attribute');
            $select2.empty(); // Limpiar opciones anteriores
            $select3.empty(); // Limpiar opciones anteriores
            
            $select2.append($('<option></option>'));
            $select3.append($('<option></option>'));
            $.each(attributes, function(index, attribute) {
                if (attribute.type == 'numeric'){
                    $select2.append($('<option></option>')
                        .attr('value', JSON.stringify(attribute))
                        .text(`${attribute.name} (${attribute.type})`));
                    $select3.append($('<option></option>')
                        .attr('value', JSON.stringify(attribute))
                        .text(`${attribute.name} (${attribute.type})`));
                }
            });
        }
    });

    var intensity = dataJson
    var y = {}
    var x = {}
    

    $('#second-attribute').change(function() {
        y = JSON.parse($('#second-attribute').val());
    });

    $('#third-attribute').change(function() {
        x = JSON.parse($('#third-attribute').val());


        final_json = {
            id: dataset_id,
            intensity: intensity.name,
            y: y.name,
            x: x.name,
        };
    
        final_json.plot = "heatmap";
        final_json.generate = 'GenerateHeatmap';
    
    
        //final JSON requirements: .generate .plot 
        active_json = final_json;
        
        //alert(JSON.stringify(final_json));
        ActivarGuardar();

    });
    
}



function RenderHeatmap(containerId, data) {
    // Cargar el contenedor del mapa
    const container = document.getElementById(containerId);

    if (!container) {
        console.error('No se encontró un contenedor con el ID proporcionado');
        return;
    }

    // Configuración del mapa con MapLibre GL JS
    const map = new maplibregl.Map({
        container: containerId, // ID del contenedor del mapa
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json', // Estilo del mapa
        center: data.center, // Coordenadas iniciales [longitud, latitud]
        zoom: 10, // Nivel de zoom inicial
    });

    // Agregar controles de navegación al mapa
    map.addControl(new maplibregl.NavigationControl(), 'top-right');

    map.on('load', function () {
        // Crear un objeto GeoJSON para los datos
        const geoJsonData = {
            type: 'FeatureCollection',
            features: data.x.map((x, index) => ({
                type: 'Feature',
                geometry: {
                    type: 'Point',
                    coordinates: [x, data.y[index]],
                },
                properties: {
                    intensity: data.intensity[index],
                },
            })),
        };

        // Agregar la fuente GeoJSON al mapa
        map.addSource('heatmap-source', {
            type: 'geojson',
            data: geoJsonData,
        });

        // Obtener los valores de intensidad máxima y mínima
        const maxIntensity = data.max_intensity || 1;
        const minIntensity = data.min_intensity || 0;

        // Agregar la capa del mapa de calor
        map.addLayer({
            id: 'heatmap-layer',
            type: 'heatmap',
            source: 'heatmap-source',
            paint: {
                // Configuración de la intensidad del calor
                'heatmap-weight': ['interpolate', ['linear'], ['get', 'intensity'], minIntensity, 0, maxIntensity, 1],
                // Difusión del calor
                'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 22, 3],
                // Radio de los puntos
                'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 2, 22, 50],
                // Opacidad del mapa de calor
                'heatmap-opacity': ['interpolate', ['linear'], ['zoom'], 0, 1, 22, 0],
                // Gradiente de colores para la intensidad del calor
                'heatmap-color': [
                    'interpolate',
                    ['linear'],
                    ['heatmap-density'],
                    0, 'rgba(33,102,172,0)',
                    0.2, 'rgb(170, 144, 215)',
                    0.4, 'rgb(131, 162, 255)',
                    0.6, 'rgb(64, 228, 212)',
                    0.8, 'rgb(197, 255, 97)',
                    1, 'rgb(38, 210, 61)'
                ],
            },
        });

        // Agregar una capa de puntos opcional para visualizar individualmente los datos
        map.addLayer({
            id: 'point-layer',
            type: 'circle',
            source: 'heatmap-source',
            paint: {
                'circle-radius': ['interpolate', ['linear'], ['get', 'intensity'], minIntensity, 3, maxIntensity, 10],
                'circle-color': 'rgba(0, 0, 0, 0)',
                'circle-stroke-width': 1,
                'circle-stroke-color': '#ffffff',
            },
        });
    });

    // Ajustar el widget del contenedor
    let widgetElement = $('#widget-' + containerId);
    var widgetIndex = widgetElement.index();
    var widget = grid.getGridItems()[widgetIndex];
    grid.update(widget, { noResize: true, noMove: true });
    //alert(containerId + ' ' + widgetIndex);
}





function GenerateHeatmap(id, json) {
    //alert("dr")
    $.ajax({
        url: '/query',           // URL a la que se envía la solicitud
        type: 'POST',            // Método de envío
        contentType: 'application/json', // Tipo de contenido que se está enviando
        data: JSON.stringify(json),  // Convertir el objeto JSON a un string JSON
        success: function(response) { // Función a ejecutar si la solicitud es exitosa
            $('#placeholder-' + id).remove();
            RenderHeatmap("widget-body-" + id, response); // Solo pasa la respuesta directamente
        },
        error: function(xhr, status, error) { // Función a ejecutar en caso de error en la solicitud
            alert('Error: ' + error);
        }
    });
}
