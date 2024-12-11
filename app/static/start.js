$(document).ready(function () {
 
$(document).on("mouseenter", ".ojo", function () {
    $(this).addClass("pulse");
  });

  $(document).on("mouseleave", ".ojo", function () {
    $(this).removeClass("pulse");
  });

});
  