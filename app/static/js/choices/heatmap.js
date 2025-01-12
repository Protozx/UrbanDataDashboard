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
                <div class="mt-4 mb-4">
                <label for="second-attribute" class="form-label">Latitude</label>
                <select id="second-attribute" class="select2" name="state" style="width: 100%" placeholder="Choose an attribute">
                    <option></option>
                </select>
                </div>

                <div class="mb-4">
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
        center: [0, 0], // Coordenadas iniciales [longitud, latitud]
        zoom: 2, // Nivel de zoom inicial
    });

    // Agregar controles de navegación al mapa
    map.addControl(new maplibregl.NavigationControl(), 'top-right');

    map.on('load', function () {
        // Agregar puntos al mapa como una fuente GeoJSON
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

        // Agregar la fuente al mapa
        map.addSource('points', {
            type: 'geojson',
            data: geoJsonData,
        });

        // Agregar una capa para renderizar los puntos
        map.addLayer({
            id: 'points-layer',
            type: 'circle',
            source: 'points',
            paint: {
                'circle-radius': 6, // Tamaño del círculo ajustado
                'circle-color': '#ffffff', // Centro blanco del círculo
                'circle-stroke-width': 2, // Grosor del borde verde
                'circle-stroke-color': '#7CFC00', // Color del borde verde claro (LawnGreen)
            },
        });
    });


    let widgetElement = $('#widget-' + containerId);

    var widgetIndex = widgetElement.index();
    var widget = grid.getGridItems()[widgetIndex];
    grid.update(widget, { noResize: true, noMove: true });
    alert(containerId + ' ' + widgetIndex)

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
