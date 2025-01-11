function ActivarGuardar(){

    document.getElementById("save-changes").disabled = false;

}

function DesactivarGuardar(){

    document.getElementById("save-changes").disabled = false;

}

function updateWidget(id, json, callback) {
    console.log(`Actualizando el widget con id: ${id}`);
    if (typeof callback === 'function') {
        callback(id, json); // Ejecuta el código que viene en los parámetros
    } else {
        console.error('El parámetro no es una función válida.');
    }
}


$(document).ready(function() {
    
    $("#save-changes").on("click", function() {
        if (!$(this).prop("disabled")) {
            //alert("updated")
            updateWidget(active_id,active_json,active_generate)
        } else {
           
        }
    });

});