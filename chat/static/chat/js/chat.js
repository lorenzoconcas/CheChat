var isMobile = false;
var dark_mode = false;
var currentChat = 0;
var unreaded_messages = 0;
var notification_sound = new Audio('/static/chat/audio/notify.ogg');

const notification = {
    thread_id: 0,
    notification_count: 0
}
let notifications = []

let push_socket = new WebSocket("ws://" + window.location.host + "/ws/push_messages");

push_socket.onopen = function(event) {
    askForMessages();
}
push_socket.onmessage = function(e) {
    let n;
    var msg = JSON.parse(e.data)
    switch(msg.type){
        case 'new_chat':{
            console.log(msg);
            $("#thread_list").append(getThreadItem(msg.name, msg.id));
            break;
        }
        case 'new_message': {
            $("#thread_preview_" + msg.chat_id).text(msg.contenuto)
            $("#thread_status_" + msg.chat_id).text("");

            notification_sound.play();

            notifyMe(e.data)
            if (currentChat == msg.chat_id) {
                divElement = getBubble(msg);
                $("#thread_bubbles").append(divElement).append("<br>");
                $(divElement).css("width", "0");
                var curHeight = $(divElement).css("height");

                $(divElement).css("height", "0");

                $("#thread_bubbles").animate({
                    scrollTop: $('#thread_bubbles').prop("scrollHeight")
                }, 1000);
                $(divElement).animate({
                    width: "45%",
                    height: curHeight
                }, 250, function () {
                });
            } else {

                let new_thread_title = "";
                unreaded_messages++;
                if (notifications.length == 0) {
                    n = Object.create(notification);
                    n.thread_id = msg.chat_id;
                    n.notification_count++;
                    notifications.push(n);
                    new_thread_title = $("#thread_title_" + msg.chat_id).text() + " (1)"

                } else {
                    let size = notifications.length;

                    for (let i = 0; i < size; i++) {
                        n = notifications[i];
                        if (n.thread_id == msg.chat_id)
                            n.notification_count++;
                        else {
                            n = Object.create(notification);
                            n.thread_id = msg.chat_id;
                            n.notification_count++;
                            notifications.push(n);
                        }
                        new_thread_title = $("#thread_title_" + n.thread_id).text() + " (" + n.notification_count + ")"

                    }

                }
                $("#thread_title_" + n.thread_id).text(new_thread_title);
            }
            if (unreaded_messages > 0)
                document.title = "Nuovo messaggio (" + unreaded_messages + ")";

            break;
        }
    }
}

function funcs() {
    //toggleTheme();

    isMobile = $("#user_name").css("visibility") == "hidden" ? true : false;

    $("#chat_title").text($("#chat_thread_1").text());
    if (isMobile)
        getPersonalID();
}

function askForMessages() {
    let message = JSON.stringify({
        'ready': 'True'
    })
    push_socket.send(message);
}
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
        url: "info/",
        data: {
            'msg': 'personal_id'
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
            url: "/sendmessage/",
            data: {
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

function closePanel(panel_name) {
    $("#" + panel_name).css("top", "150%");
}

function openPanel(panel_name) {
    if (isMobile)
        $("#" + panel_name).css("top", 0);
    else
        $("#" + panel_name).css("top", "25%");
}

function openInputPanel() {
    //
    if (isMobile)
        openPanel("input_panel");
    else {
        $("#input_panel").css("top", "calc(50% - 50px)");
        $("#input_panel").css("top", "calc(50% - 50px)");
    }

    $("#input_panel").css("height", "100px");
    $("#input_panel_error").hide();
    $("#input_panel_title").text("Nuovo contatto");
    $("#input_panel_text").attr("placeholder", "Inserisci un indirizzo mail");
    $("#input_panel_btn_confirm").on("keypress", addContact2);
    $("#input_panel_btn_confirm").click(addContact);

}

function openCECPanel(mode) {
    openPanel("chat_and_contacts_panel");

    if (mode) { //se nuova chat
        $("#cec_title").text("Nuova Chat");
        $("#contacts_list").css("height", "calc(100% - 98px)");
        $("#cec_footer").hide();
        $(".contact_checkbox").show();
        $(".contact_delete").hide();
    } else {
        $("#cec_title").text("Rubrica");
        $("#contacts_list").css("height", "calc(100% - 132px)");
        $("#cec_footer").show();
        $(".contact_checkbox").hide();
        $(".contact_delete").show();
    }
}

function closeChatThread() {
    if (isMobile) {
        $("#chat").css("left", "100%");
        $("#new_thread").hide();
        $(".chat_thread").css("background", "transparent");
        $("#thread_bubbles").empty();
        currentChat = 0;
    }


}

function openThread(chat_id) {
    if (isMobile) {
        $("#chat").css("left", "0");
        $("#new_thread").hide();

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

    $("#thread_status_" + chat_id).text("");
    $(".chat_thread").css("background", "transparent");
    $("#chat_title").text($("#thread_title_" + chat_id).text());

    $("#thread_" + chat_id).css("background", "dodgerblue");

    $("#chat").show();
    loadMessages(chat_id);
    window.location = "#";


}

function loadMessages(chat_id) {
    $.ajax({
        type: "POST",
        url: "/allmessages/",
        data: {
            'chat_id': chat_id
        },
        beforeSend: function(request, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                request.setRequestHeader("X-CSRFToken", csrfcookie());
            }
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
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

function getBubble(messaggio) {
    var bubble = document.createElement("div");
    $(bubble).addClass("bubble_container");

    if (messaggio.inviato == "True")
        $(bubble).addClass("outgoing");
    else
        $(bubble).addClass("incoming");

    if (messaggio.mittente != "") {
        var mittente = document.createElement("label")
        $(mittente).text(messaggio.mittente);
        $(mittente).addClass("bubble_sender_name");
        $(bubble).append(mittente);
        $(bubble).append("<br>");
    }


    var msg = document.createElement("label");
    $(msg).text(messaggio.contenuto);
    $(bubble).append(msg);

    return bubble;
}

function openChatThreadDetail() {
    alert("to do");
}

function toggleTheme() {

    if (dark_mode) {
        dark_mode = false;
        document.getElementById('theme').href = "/static/chat/css/light.css";
        document.getElementById("theme_mode_btn").innerText = "";
    } else {
        dark_mode = true;
        document.getElementById("theme").href = "/static/chat/css/dark.css";
        document.getElementById("theme_mode_btn").innerText = "";
    }
    if (isMobile)
        B4A.CallSub('darkMode', true, dark_mode + "")
}

function tooltip(wich, visible) {
    status = visible ? "visible" : "hidden";
    $("#" + wich).css("visibility", status);
}

function addContact() {
    $("#input_panel").css("height", "100px");

    $("#input_panel_error").show();
    $("#input_panel_error").css("visibility", "hidden");
    $("#input_panel_error").text("");
    let mail = $("#input_panel_text").val();
    $.ajax({
        type: "POST",
        url: "send_data/",
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

function addContact2() {
    if (e.keyCode === 13) {
        addContact()
    }
}

function removeFromContacts(id){

    $.ajax({
        type: "POST",
        url: "send_data/",
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

function startChat(){
    var chat_ids = [];
    $('#contacts_list input:checked').each(function() {
        var id = $(this).attr('id');
        id = id.replace("c_", "");
        console.log(id);
        chat_ids.push(id);
    });
    var chat_ids_json = JSON.stringify(chat_ids);
    $.ajax({
        type: "POST",
        url: "send_data/",
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
            /*
            * <div         class="chat_thread"  id="thread_{{ chat_thread.chat_id }}" onclick="openThread({{ chat_thread.chat_id }})">
                    <img   class="thread_icon"     src="{% static 'chat/icons/generic_user.png' %}" alt="username">
                    <label class="thread_title"  id="thread_title_{{ chat_thread.chat_id }}">{{ chat_thread.chat.nome }}</label>
                    <label class="thread_status" id="thread_status_{{ chat_thread.chat_id }}"></label>
                    <br>
                    <label class="thread_preview" id="thread_preview_{{ chat_thread.chat_id }}">{{ chat_thread|getltsmsg:"32" }}</label>
                </div>
            *
            * */
            console.log(data);
            if(data[0].result == "ok"){
                closePanel("chat_and_contacts_panel");
             //   $("#thread_list").append(getThreadItem(data[0].name, data[0].id));
                //vengono aggiunti automaticamente in push su tutti i dispositivi
            }

        }
    });

}

function getThreadItem(chat_name, id) {
  let div = document.createElement("div");
                let img = document.createElement("img");
                let name = document.createElement("label");
                let status = document.createElement("label");
                let preview = document.createElement("label");

                $(div).addClass("chat_thread");

                $(img).attr("src", "/static/chat/icons/generic_user.png"); //modificare con icona gruppi
                $(img).addClass("thread_icon")
                $(name).text(chat_name);
                if (chat_name.length > 28) {
                    $(name).text(chat_name.substring(0, 28) + '...');
                     $(name).css("font-size", "16px");
                }
                $(name).addClass("thread_title");
                $(status).addClass("thread_status");
                $(preview).addClass("thread_preview");
                $(name).attr("id", "thread_title_"+id);
                $(status).attr("id", "thread_status_"+id);
                $(status).text("")
                $(preview).addClass("id", "thread_preview_"+id);


                $(div).append(img);
                $(div).append(name);
                $(div).append(status);
                $(div).append("<br>");
                $(div).append(preview);


                $(div).attr("id", "thread_"+id);
                $(div).attr("onclick", "openThread("+id+")");
   return div
}