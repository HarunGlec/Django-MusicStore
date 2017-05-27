$(function(){
  $('#paylas_butonu').click(function(e) {
    var counter = $.trim($('#yazi_alani').val()).length;
    if (counter == 0) {
      e.preventDefault();
      alert("Lütfen boş girme");
    }
  });

  $('#profil_resmi').click(function(e) {
    e.preventDefault();
    var karanlik = $('.karanlik');
    karanlik.fadeIn(300);
  });

  $('.karanlik').click(function() {
    $('.karanlik').fadeOut(300);
  });

});
