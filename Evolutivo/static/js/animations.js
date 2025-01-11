$(document).ready(function () {
 
  $(document).on("mouseenter", ".icon", function () {
    $(this).removeClass("iblanco");
    $(this).addClass("pulse iazul");
  });

  $(document).on("mouseleave", ".icon", function () {
    $(this).removeClass("pulse iazul");
    $(this).addClass("iblanco");
  });

  $(document).on("mouseenter", ".icon-black", function () {
    $(this).removeClass("inegro");
    $(this).addClass("pulse iazul");
  });

  $(document).on("mouseleave", ".icon-black", function () {
    $(this).removeClass("pulse iazul");
    $(this).addClass("inegro");
  });


    // Detectar cuando un botón tiene el atributo "disabled"
    $('button').each(function() {
        if ($(this).is(':disabled')) {
            $(this).addClass('forbidden');
        }
    });

    // Observa cambios en el atributo "disabled"
    $(document).on('DOMSubtreeModified', 'button', function() {
        if ($(this).is(':disabled')) {
            $(this).removeClass('btn-primary');
            $(this).addClass('forbidden btn-secondary');
        } else {
            $(this).removeClass('forbidden btn-secondary');
            $(this).addClass('btn-primary');
        }
    });


});
  