(function($) {

$(document).ready(function(){
    $("#form_set_status").on("click", "#button__set_status", {form : "#form_set_status"}, change_state);
});


function change_state(event){
    console.log(event.data)
    var form = $(event.data.form)
    var csrf = getCookie('csrftoken');
    var url = form.attr("action");
    var values = form.serializeArray();
    console.log(form)
    $.ajax({
            data: values,
            type: form.attr("method"),
            url: url,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                }
            },
            success: function(json){
                if (json.action=='error'){
                    alert('Ничё не заполнилось');
                    $(field).val($(field).data('val'));
                    fading($(field).next('span'), 'Error')
                    return false;
                }
                if (json.action=='ok'){
                   alert('Все хорошо');
                   $(field).val(json.cost);
                   $(field).data('val', json.cost);
                   console.log($(field).data('val'));
                   fading($(field).next('span'), 'Ok')
                }
            }
    });
    return false;
}


function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


})(jQuery);