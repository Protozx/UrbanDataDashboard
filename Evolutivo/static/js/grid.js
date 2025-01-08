$(document).ready(function () {

    var grid = GridStack.init({
        margin: 2 // Espacio en píxeles entre los grids
    });
    //grid.addWidget({w: 2, content: 'item 1'});

    let widgetCounter = 0; // Contador global para IDs dinámicos

    $(document).on("click", "#add-widget", function () {
        // Generar un ID dinámico basado en el contador
        widgetCounter = widgetCounter + 1

        // Crear el widget con su ID
        let widget = grid.addWidget(`
        <div id="widget-${widgetCounter}" class="grid-stack-item">
          <div class="grid-stack-item-content shadow rounded-2 bg-white m-1 d-flex align-items-center justify-content-center w-95 h-95">
            <i class="fa-solid fa-chart-simple fa-2xl big-1 iazul widget" data-number="${widgetCounter}"></i>
          </div>
        </div>`,
            { w: 2, h: 2 }); // Dimensiones del widget

        // Opcional: imprimir el ID para verificar
        console.log("Widget añadido con ID:", widgetCounter);
    });

    // In your Javascript (external .js resource or <script> tag)

    $('.select-source').select2({
        width: 'resolve',
        dropdownParent: $('#miModal') // need to override the changed default
    });

    $(document).on("click", ".widget", function () {
        // Obtener el valor de data-number
        var dataNumber = $(this).data('number');
        console.log(dataNumber)
        // Asignar el valor al h5 dentro del modal
        $('#miModalLabel').text('Widget ' + dataNumber + ' settings');
        
        // Abrir el modal utilizando Bootstrap 5
        var myModal = new bootstrap.Modal($('#miModal')[0]);
        myModal.show();
    });

































});






