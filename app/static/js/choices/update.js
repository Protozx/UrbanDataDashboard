var plot = {};

//DECLARAR TODOS LOS TIPOS DE FUNCION
plot.GenerateTimeseries = GenerateTimeseries








function ActivarGuardar(){

    document.getElementById("save-changes").disabled = false;

}

function DesactivarGuardar(){

    document.getElementById("save-changes").disabled = false;

}

function updateWidget(id) {

    json = JSON.parse($('#json-' + id ).val());
    callback = plot[json.generate];

    console.log(`Actualizando el widget con id: ${id}`);


    alert(JSON.stringify(json))
    if (typeof callback === 'function') {
        callback(id, json); // Ejecuta el código que viene en los parámetros
        alert(terminé, json.generate)
    } else {
        console.error('El parámetro no es una función válida.');
    }
}


$(document).ready(function() {
    
    $("#save-changes").on("click", function() {
        if (!$(this).prop("disabled")) {
            //alert("updated")
            $('#json-' + active_id ).val(JSON.stringify(active_json));
            updateWidget(active_id)
        } else {
           
        }
    });

});