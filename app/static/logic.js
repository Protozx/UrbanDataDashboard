

$(document).ready(function () {
          
 
    $(document)
      .on("mouseenter", ".pulsblue", function () {
        $(this).addClass("btn-primary pulse");
      })
      .on("mouseleave", ".pulsblue", function () {
        $(this).removeClass("btn-primary pulse");
      });
  
    $(document)
      .on("mouseenter", ".pulsred", function () {
        $(this).removeClass("btn-secondary");
        $(this).addClass("btn-danger text-white pulse");
      })
      .on("mouseleave", ".pulsred", function () {
        $(this).removeClass("btn-danger text-white pulse");
        $(this).addClass("btn-secondary");
      });
  
    $(document)
      .on("mouseenter", ".pulscyan", function () {
        $(this).removeClass("btn-secondary");
        $(this).addClass("btn-primary text-white pulse");
      })
      .on("mouseleave", ".pulscyan", function () {
        $(this).removeClass("btn-primary text-white pulse");
        $(this).addClass("btn-secondary");
      });
  
    $(document)
      .on("mouseenter", ".pulsgreen", function () {
        $(this).removeClass("btn-dark text-white");
        $(this).addClass("btn-info text-black pulse");
      })
      .on("mouseleave", ".pulsgreen", function () {
        $(this).removeClass("btn-info text-black pulse");
        $(this).addClass("btn-dark text-white");
      });
  
    $(document)
      .on("mouseenter", ".actualizar", function () {
        $(this).removeClass("iblanco");
        $(this).addClass("iazul pulse spin");
      })
      .on("mouseleave", ".actualizar", function () {
        $(this).removeClass("iazul pulse spin");
        $(this).addClass("iblanco");
      });
  
    $(document)
      .on("mouseenter", ".eliminar", function () {
        $(this).removeClass("iblanco");
        $(this).addClass("irojo pulse");
      })
      .on("mouseleave", ".eliminar", function () {
        $(this).removeClass("irojo pulse");
        $(this).addClass("iblanco");
      });
  
    $(document).on("mouseenter", ".ojo", function () {
      $(this).addClass("big");
    });
  
    $(document).on("mouseleave", ".ojo", function () {
      $(this).removeClass("big");
    });
  
    $(document).on("click", ".eliminar", function () {
      var numero = $(this).attr("data-id");
      $("#chunche" + numero).addClass("d-none");
    });
  
    
  
    $(document).on("click", "#modo1", function () {
      var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
      <strong>Modo 1</strong> Sliders generales
    </div>`);
      nuevoElemento.appendTo("#alertas");
      setTimeout(function () {
        nuevoElemento.remove();
      }, 3000);
      cambiarmodo(1);
      modo = 1;
    });
  
    $(document).on("click", "#modo2", function () {
      var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
      <strong>Modo 2</strong> Variable dependiente
    </div>`);
      nuevoElemento.appendTo("#alertas");
      setTimeout(function () {
        nuevoElemento.remove();
      }, 3000);
      cambiarmodo(2);
      modo = 2;
    });
  
    $(document).on("click", "#modo3", function () {
      var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
      <strong>Modo 3</strong> Variable independiente
    </div>`);
      nuevoElemento.appendTo("#alertas");
      setTimeout(function () {
        nuevoElemento.remove();
      }, 3000);
      cambiarmodo(3);
      modo = 3;
    });
  
    $(document).on("click", "#modo5", function () {
      var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
      <strong>Modo 5</strong> Relaciones
    </div>`);
      nuevoElemento.appendTo("#alertas");
      setTimeout(function () {
        nuevoElemento.remove();
      }, 3000);
      cambiarmodo(5);
      modo = 5;
    });
  
    $(document).on("click", "#modo6", function () {
      var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
      <strong>Modo 6</strong> Filtros
    </div>`);
      nuevoElemento.appendTo("#alertas");
      setTimeout(function () {
        nuevoElemento.remove();
      }, 3000);
      cambiarmodo(6);
      modo = 6;
    });
  
    $(document).on("click", "#modo7", function () {
      var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
      <strong>Modo 6</strong> Procesar / operar 
    </div>`);
      nuevoElemento.appendTo("#alertas");
      setTimeout(function () {
        nuevoElemento.remove();
      }, 3000);
      cambiarmodo(7);
      modo = 7;
    });
  
    $(document).on("blur", ".libre", function () {
      var valor = parseFloat($(this).val());
      if (isNaN(valor) || valor < $(this).attr("min")) {
        $(this).val($(this).attr("min"));
      } else if (valor > $(this).attr("max")) {
        $(this).val($(this).attr("max"));
      }
    });
  
    $(document).on("click", ".operar", function () {
      iniciarop($(this).attr("data-id"), $(this).attr("data-op"));
    });
  
    $(document).on("click", ".operar2", function () {
      op2 = $(this).attr("data-id");
      operar();
      terminarop(op1);
    });
  
    $(document).on("click", ".desoperar", function () {
      terminarop($(this).attr("data-id"));
    });
  
    $(document).on("click", ".integrar", function () {
      id = $(this).attr("data-id");
      filtrar(id, 2);
    });
  
    $(document).on("click", ".reflexion", function () {
      id = $(this).attr("data-id");
      filtrar(id, 8);
    });
  
    $(document).on("click", ".diferenciar", function () {
      id = $(this).attr("data-id");
      filtrar(id, 3);
    });
  
    $(document).on("click", ".filtro1", function () {
      id = $(this).attr("data-id");
      filtrar(id, 1);
    });
  
    $(document).on("click", ".filtrar", function () {
      id = $(this).attr("data-id");
      filtro = $(this).attr("data-modo");
      filtrar(id, filtro);
    });
  
    $(document).on("input", ".gordo", function () {
      id = $(this).attr("data-id");
      $("#img" + id).text($(this).val());
    });
  
  });
  