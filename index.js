$(document).ready(function(){
    if (window.innerWidth/2 < 650) {
        width = innerWidth
        $('#form-con').removeClass('web-width')
        $('#form-con').addClass('mobile-width')
    } else {
        width =  window.innerWidth/2
    }

    $( "#dialog" ).dialog({
        width: width
    });
});