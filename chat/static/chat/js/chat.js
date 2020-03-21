let isMobile = false;
let dark_mode = false;
let currentChat = 0;
let unreaded_messages = 0;

function setup() {
    //calcolo se ci troviamo su un dispositivo mobile o a vista singola
    isMobile = $("#user_name").css("visibility") == "hidden" ? true : false;

    $("#chat_title").text($("#chat_thread_1").text());
    if (isMobile)
        getPersonalID();
}

//il cookie per le chiamate POST
let csrfcookie = function() {
    let cookieValue = null,
        name = "csrftoken";
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function getPersonalID() {
    $.ajax({
        type: "POST",
        url: "client_reqs/",
        data: {
            'req': 'personal_id'
        },
        dataType: 'json',
        beforeSend: function(request, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                request.setRequestHeader("X-CSRFToken", csrfcookie());
            }
        },
        success: function(data) {
            B4A.CallSub('SetID', false, data)
        },
    });
}

function sendMessage() {
    var msg = document.getElementById("message_box");
    if (msg.value !== '') {
        $.ajax({
            type: "POST",
            url: "client_reqs/",
            data: {
                'req' : 'send_message',
                'msg': msg.value,
                'chat_id': currentChat
            },
            beforeSend: function(request, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    request.setRequestHeader("X-CSRFToken", csrfcookie());
                }
            },
            success: function(data) {
                console.log(data)

            },
        });

        var br = document.createElement("br");
        var msg_text = document.createElement("label");
        msg_text.textContent = msg.value;
        var msg_bubble = document.createElement("div");

        msg_bubble.appendChild(msg_text);
        $(msg_bubble).addClass("lastElement");
        var target = document.getElementById("thread_bubbles");

        var bubble_clone = $(msg_bubble).clone();

        $(bubble_clone).addClass("bubble_container");
        $(bubble_clone).addClass("outgoing");
        if (isMobile) {
            $(bubble_clone).appendTo(target);
            target.appendChild(br).scrollIntoView(true);
        } else {
            var bcW = $(bubble_clone).css("width");
            $(bubble_clone).addClass("bubble_container");
            $(bubble_clone).addClass("outgoing");
            $(bubble_clone).css("opacity", "0");
            $(bubble_clone).appendTo(target);
            target.appendChild(br).scrollIntoView(true);

            $(msg_bubble).addClass("moving_bubble");

            $("#send_box").append(msg_bubble);

            $(msg_bubble).animate({
                top: "-42px",
                left: "52%",
                width: "-=240px",
                height: "-=6px",

            }, 250, "linear", function() {
                $(bubble_clone).animate({
                        opacity: 1,
                    },
                    250,
                    "linear",
                    function() {
                        $(msg_bubble).fadeTo(350, 0);

                        target.appendChild(br).scrollIntoView(true);
                        $(msg_bubble).remove();
                    }
                )
            });
        }
         $("#thread_preview_"+currentChat).text("Tu: "+msg.value.substring(0, 20));
        msg.value = '';
    }

}
function sendMessageOnEnter(e) {
    if (e.keyCode === 13) {
        var msg = document.getElementById("message_box");
        e.preventDefault();
        sendMessage();
    }

}

function openThread(chat_id) {
    if (isMobile) {
        $("#chat").css("left", "0");
       // $("#new_thread").css("visibility", "hidden");
        $("#new_thread").toggle(250);
    }else{
        $("#thread_status_" + chat_id).text("");
        $(".chat_thread").css("background", "transparent");
        $("#chat_title").text($("#thread_title_" + chat_id).text());
        $("#thread_" + chat_id).css("background", "dodgerblue");
    }
    currentChat = chat_id;

    let size = notifications.length;
    for (let i = 0; i < size; i++) {
        let n = notifications[i];
        if (n.thread_id == chat_id) {
            let actual_title = $("#thread_title_" + n.thread_id).text()
            let new_thread_title = actual_title.replace('- (' + n.notification_count + ')')
            $("#thread_title_" + n.thread_id).text(new_thread_title);
            unreaded_messages = unreaded_messages - n.notification_count;
            n.notification_count = 0;
        }
    }

    unreaded_messages > 0 ? document.title = "Nuovo messaggio (" + unreaded_messages + ")" : document.title = "ISW Chat"

    $("#chat").show();
    loadMessages(chat_id);
}
function loadMessages(chat_id) {
    $.ajax({
        type: "POST",
        url: "client_reqs/",
        data: {
            'req' : 'getAllMessages',
            'chat_id': chat_id
        },
        beforeSend: function(request, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                request.setRequestHeader("X-CSRFToken", csrfcookie());
            }
        },
        dataType: 'json',
        success: function(data) {
          //  console.log(data);
            $("#thread_bubbles").empty();
            $("#thread_bubbles").append("<br>");
            $("#thread_bubbles").append("<br>");
            $("#thread_bubbles").append("<br>");
            for (var messaggio in data) {
                $("#thread_bubbles").append(getBubble(data[messaggio]));
                $("#thread_bubbles").append("<br>");
            }
            $("#chat").css("visibility", "visible");
            /*   var objDiv = document.getElementById("thread_bubbles");
                objDiv.scrollTop = objDiv.scrollHeight;*/
            $("#thread_bubbles").animate({
                scrollTop: 10000000000000,
            }, 125);

        },
    });
}

//utilizzate per salvare un nuovo contatto in rubrica
function addContact() {
    hideInputPanel();
    let mail = $("#input_panel_text").val();
    $.ajax({
        type: "POST",
        url: "client_reqs/",
        data: {
            'req' : 'add_contact',
            'mail': mail,
        },

        beforeSend: function(request, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                request.setRequestHeader("X-CSRFToken", csrfcookie());
            }
        },
         dataType: 'json',
        success: function(data) {
            if (data[0].result == "ok"){
                closePanel("input_panel");

                let div = document.createElement("div");
                let checkbox = document.createElement("input"); checkbox.type = 'checkbox';
                let img = document.createElement("img");
                let name = document.createElement("label");
                let del_btn = document.createElement("button");

                $(div).addClass("contact_element");
                $(checkbox).addClass("contact_checkbox");
                $(checkbox).attr("id", data[0].id)
                $(img).attr("src", "/static/chat/icons/generic_user.png");
                $(img).addClass("contact_icon")
                $(name).text(data[0].name);
                $(name).addClass("contact_name");
                $(del_btn).addClass("contact_delete");
                $(del_btn).text("")

                $(div).append(checkbox);
                $(checkbox).hide();
                $(div).append(img);
                $(div).append(name);
                $(div).append(del_btn);

                $(div).attr("id", "contact_"+data[0].id);
                $("#contacts_list").append(div);

            }
            else{
                //<label id="input_panel_error">Errore</label>
                $("#input_panel").css("height", "120px");
                $("#input_panel_error").show();
                $("#input_panel_error").css("visibility", "visible");
                $("#input_panel_error").text(data[0].error);
            }
        },
    });
}
//alla pressione del tasto invio
function addContact2() {
    if (e.keyCode === 13) {
        addContact()
    }
}
//auto esplicativa
function removeFromContacts(id){

    $.ajax({
        type: "POST",
        url: "client_reqs/",
        data: {
            'req' : 'remove_contact',
            'id': id,
        },

        beforeSend: function(request, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                request.setRequestHeader("X-CSRFToken", csrfcookie());
            }
        },
        success: function(data) {
            $("#contact_"+id).remove();
        },
    });

}
//crea una nuova chat dati i contatti selezionati
function startChat(){
    var chat_ids = [];
    $('#contacts_list input:checked').each(function() {
        var id = $(this).attr('id');
        id = id.replace("c_", "");
        console.log(id);
        chat_ids.push(id);
    });
    if(chat_ids.length > 0) {
        var chat_ids_json = JSON.stringify(chat_ids);
        $.ajax({
            type: "POST",
            url: "client_reqs/",
            data: {
                'req': 'create_chat',
                'user_ids_json': chat_ids_json,
            },

            beforeSend: function (request, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    request.setRequestHeader("X-CSRFToken", csrfcookie());
                }
            },
            dataType: 'json',
            success: function (data) {

                console.log(data);
                if (data[0].result == "ok") {
                    closePanel("chat_and_contacts_panel");
                    $("#thread_list").append(getThreadItem(data[0].name, data[0].id));
                    //vengono aggiunti automaticamente in push su tutti i dispositivi
                    openThread(data[0].id);
                }

            }
        });
    }
}

function deleteChat(){
    if(currentChat == 0)
        return;


}

function addPartecipant() {

}