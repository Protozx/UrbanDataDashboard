document.addEventListener("DOMContentLoaded", function () {
    // Inicializar Gridstack
    const grid = GridStack.init({
      cellHeight: 80,
      // Tamaño por defecto 5x5 (para simplificar, 
      // gridstack utiliza 'minRow'/'maxRow' o 'column' para limitar columnas)
      column: 5, 
      float: true,
    });
  
    // Botón para agregar widget al grid
    const addWidgetBtn = document.getElementById("add-widget-btn");
    addWidgetBtn.addEventListener("click", function () {
      // Crear un ID único para el widget
      const widgetId = "widget-" + Date.now();
  
      // Agregar el widget a la grid
      let widget = grid.addWidget({
        x: 0,
        y: 0,
        w: 1,
        h: 1,
        content: `
          <div class="card h-100">
            <div class="card-body d-flex flex-column justify-content-center align-items-center">
              <button class="btn btn-primary configure-btn" data-widget-id="${widgetId}">
                Configurar
              </button>
            </div>
          </div>
        `,
      });
  
      // Asignar un id al contenedor interno (para luego insertar el canvas)
      widget.el.setAttribute("id", widgetId);
    });
  
    // Manejo del botón "Configurar"
    // Usamos event delegation (delegación de eventos) 
    // ya que los widgets se crean dinámicamente
    document.addEventListener("click", function (event) {
      if (event.target.matches(".configure-btn")) {
        const widgetId = event.target.dataset.widgetId;
        // Guardamos el ID del widget que se está editando
        document.getElementById("currentWidgetId").value = widgetId;
        // Abrimos el modal de configuración
        const chartConfigModal = new bootstrap.Modal(
          document.getElementById("chartConfigModal")
        );
        chartConfigModal.show();
      }
    });
  
    // Botón del modal para guardar la configuración
    const saveChartConfigBtn = document.getElementById("saveChartConfig");
    saveChartConfigBtn.addEventListener("click", function () {
      const widgetId = document.getElementById("currentWidgetId").value;
      const chartType = document.getElementById("chartTypeSelect").value;
  
      if (!widgetId || !chartType) return;
  
      // Llamar a la ruta de Flask para obtener datos
      $.ajax({
        url: "/get_chart_data",
        method: "POST",
        data: { chartType: chartType },
        success: function (response) {
          // Insertar la gráfica en el widget
          renderChartInWidget(widgetId, chartType, response);
        },
        error: function (xhr, status, error) {
          console.error("Error al obtener datos de la gráfica:", error);
        },
      });
    });
  
    function renderChartInWidget(widgetId, chartType, data) {
      const widgetEl = document.getElementById(widgetId);
      if (!widgetEl) return;
  
      // Limpiar contenido para insertar un canvas
      widgetEl.querySelector(".card-body").innerHTML = `
        <canvas id="canvas-${widgetId}"></canvas>
      `;
  
      // Crear instancia de Chart.js
      const ctx = document.getElementById(`canvas-${widgetId}`).getContext("2d");
  
      // Definir configuración base
      let config = {
        type: chartType === "bar" ? "bar" : "pie",
        data: {
          labels: data.labels,
          datasets: [
            {
              label: "Dataset",
              data: data.values,
              backgroundColor: chartType === "bar"
                ? ["rgba(54, 162, 235, 0.5)"]
                : [
                    "rgba(255, 99, 132, 0.5)",
                    "rgba(54, 162, 235, 0.5)",
                    "rgba(255, 206, 86, 0.5)",
                    "rgba(75, 192, 192, 0.5)",
                  ],
              borderColor: chartType === "bar"
                ? ["rgba(54, 162, 235, 1)"]
                : [
                    "rgba(255, 99, 132, 1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(75, 192, 192, 1)",
                  ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          maintainAspectRatio: false, // Para que se adapte al tamaño del grid
          responsive: true,
        },
      };
  
      new Chart(ctx, config);
    }
  
    // Ajustar el tamaño de la gráfica al redimensionar el widget
    // Gridstack emite eventos cuando se arrastra o se redimensiona
    grid.on("resizestop", function (event, elements) {
      elements.forEach(function (element) {
        let canvasEl = element.el.querySelector("canvas");
        if (canvasEl) {
          // Forzar a Chart.js a actualizar su tamaño
          canvasEl.chart?.resize();
        }
      });
    });
  });
  