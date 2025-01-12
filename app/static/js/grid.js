$(document).ready(function () {

    var grid = GridStack.init({
        margin: 2 // Espacio en píxeles entre los grids
    });
    //grid.addWidget({w: 2, content: 'item 1'});

    let widgetCounter = -1; // Contador global para IDs dinámicos

    $(document).on("click", "#add-widget", function () {
        // Generar un ID dinámico basado en el contador
        widgetCounter = widgetCounter + 1;
    
        // Crear el widget con su ID, incluyendo el tache
        let widget = grid.addWidget(`
        <div id="widget-${widgetCounter}" class="grid-stack-item">
          <div id="widget-body-${widgetCounter}" class="grid-stack-item-content shadow rounded-2 bg-white m-1 d-flex align-items-center justify-content-center w-95 h-95">
            <input type="hidden" id="json-${widgetCounter}" value="">
            <i id="placeholder-${widgetCounter}" class="fa-solid fa-chart-simple fa-2xl big-1 iazul widget" data-number="${widgetCounter}"></i>
            <span class="fa-solid fa-xmark text-danger" style="position: absolute; top: 0; right: 0; cursor: pointer;" data-remove="${widgetCounter}"></span>
          </div>
        </div>`,
            { w: 2, h: 2 }); // Dimensiones del widget
    
        // Opcional: imprimir el ID para verificar
        console.log("Widget añadido con ID:", widgetCounter);
    });
    
    // Función para eliminar un widget al hacer clic en el tache
    $(document).on("click", ".fa-xmark", function () {
        let widgetId = $(this).data('remove');
        let widgetElement = $('#widget-' + widgetId);

        //grid.removeWidget(widgetElement, true, true);
        var widgetIndex = widgetElement.index();
        var widget = grid.getGridItems()[widgetIndex];  // Reemplaza 'indice' por el índice del widget
        
        grid.removeWidget(widget);
        //widgetElement.addClass("d-none");
        //grid.removeAll();
    });


    // In your Javascript (external .js resource or <script> tag)

    $('.select-source').select2({
        width: 'resolve',
        placeholder: "Select an option",
        allowClear: false,
        dropdownParent: $('#miModal') // need to override the changed default
    });

    $(document).on("click", ".widget", function () {
        // Obtener el valor de data-number
        var dataNumber = $(this).data('number');
        console.log(dataNumber)
        // Asignar el valor al h5 dentro del modal
        $('#miModalLabel').text('Widget ' + dataNumber + ' settings');
        $('#current-id').val(dataNumber);
        active_id = $('#current-id').val();
        
        // Abrir el modal utilizando Bootstrap 5
        var myModal = new bootstrap.Modal($('#miModal')[0]);
        myModal.show();
    });

    $("#descargar-btn").on("click", function () {
        // Obtiene el contenido HTML del div con ID "big_container"
        const divContent = $("#big_container").prop("outerHTML");
        
        // Crea un Blob con el contenido
        const blob = new Blob([divContent], { type: "text/html" });
        
        // Crea un enlace temporal para descargar el archivo
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "big_container.html"; // Nombre del archivo
        link.click();
        
        // Limpia el objeto URL para liberar memoria
        URL.revokeObjectURL(link.href);
    });

    $("#cargar-btn").on("click", function () {
        // Crear dinámicamente un input file
        const inputFile = $("<input>", { type: "file", accept: ".html" });
        
        // Escuchar el cambio del archivo seleccionado
        inputFile.on("change", function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const fileContent = e.target.result;
                    // Sobrescribir el contenido del div
                    $("#big_container").replaceWith(fileContent);
                };
                reader.readAsText(file);
            }
        });
        
        // Simular clic en el input file para abrir la ventana de selección de archivos
        inputFile.trigger("click");
    });
    
    
    


















});






