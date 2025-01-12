var active_id;
var active_json;
var active_generate;

var update_list = []
var active_list = []

//update_list.push('nuevo elemento');

var grid = GridStack.init({
    margin: 2 // Espacio en píxeles entre los grids
});

$(document).ready(function() {
    setInterval(function() {
        const now = new Date();
        console.log(now.toLocaleTimeString());
        refresh()
    }, 5000); // 10000 ms = 10 segundos
});

function refresh() {
    update_list.forEach(function(id) {
        updateWidget(id);
    });
}