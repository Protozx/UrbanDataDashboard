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
  
  });
    