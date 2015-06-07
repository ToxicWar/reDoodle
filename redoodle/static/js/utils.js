$ = document.querySelector.bind(document);
$$ = document.querySelectorAll.bind(document);
Element.prototype.prependChild = function(elem){
	this.insertBefore(elem, this.firstChild);
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function send_image(canvas, room, chain, url) {
    var base64 = canvas.toDataURL();
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
            type: "POST",
            url: url,
            data: {'base64': base64, 'room': room, 'chain': chain},
            //contentType: "application/json; charset=utf-8",
            dataType: 'text',
            async: true,
            cache: false,
            success: function(data) {
                alert(data);
                if (data != 'Fail.')
                    document.location.href = '/'+room;
            },
            fail: function(data) {
                alert(data);
            }
        });
}

function like(url, chain, like) {
    like_class = '.'+chain+'_like_count .likes';
    $.ajax({
            type: "GET",
            url: url,
            data: {'chain': chain, 'like': like},
            contentType: "application/json; charset=utf-8",
            dataType: "text",
            async: true,
            cache: false,
            success: function(data) {
                $(like_class).html(data);
            },
            fail: function(data) {
                alert('Fail.');
            }
        });
}
