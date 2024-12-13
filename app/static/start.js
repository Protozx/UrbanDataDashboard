$(document).ready(function () {
 
  $(document).on("mouseenter", ".ojo", function () {
    $(this).addClass("pulse");
  });

  $(document).on("mouseleave", ".ojo", function () {
    $(this).removeClass("pulse");
  });

  $(document).on("mouseenter", ".ojo2", function () {
    $(this).addClass("big2");
  });

  $(document).on("mouseleave", ".ojo2", function () {
    $(this).removeClass("big2");
  });



});
  