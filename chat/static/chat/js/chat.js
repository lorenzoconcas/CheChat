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

    $("#thread_preview_" + msg.chat_id).text(msg.contenuto)
    $("#thread_status_" + msg.chat_id).text("");

     notification_sound.play();

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
        }, 250, function() {});
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

        if (unreaded_messages > 0)
            document.title = "Nuovo messaggio (" + unreaded_messages + ")";
    }
}


function funcs() {
    var x = document.getElementById("thread_bubbles")
    x.scrollTo(0, x.scrollHeight);
    var el = document.getElementById('navbar_title');
    var style = window.getComputedStyle(el, null).getPropertyValue('font-size');
    var fontSize = parseFloat(style);
    isMobile = fontSize >= 80 ? true : false;
    // toggleTheme();

    $("#chat_title").text($("#chat_thread_1").text());

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

function closeNewChat() {
    $("#new_chat_panel").css("top", "150%");

}

function openNewChat() {
    if (isMobile)
        $("#new_chat_panel").css("top", "128px");
    else
        $("#new_chat_panel").css("top", "25%");
}

function openThread(chat_id) {
    if (isMobile) {
        $("#chat").css("left", "0");
        $("#new_thread").css("visibility", "hidden");

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
    $("#chat_title").text($("#thread_title_"+chat_id).text());

    $("#thread_" + chat_id).css("background", "dodgerblue");

    $("#chat").css("visibility", "visible");
    loadMessages(chat_id);
    window.location = "#";

    $("#thread_bubbles").animate({
        scrollTop: 10000000000000,
    }, 250);
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

            $("#thread_bubbles").empty();
            $("#thread_bubbles").append("<br>");
            $("#thread_bubbles").append("<br>");
            $("#thread_bubbles").append("<br>");
            for (var messaggio in data) {
                $("#thread_bubbles").append(getBubble(data[messaggio]));
                $("#thread_bubbles").append("<br>");
            }

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
}

function showtooltip(wich) {
    switch (wich) {
        case 0: {
            $("#tooltip_exit").css("visibility", "visible");
            break;
        }
        case 1: {
            $("#tooltip_edit_profile").css("visibility", "visible");
            break;
        }

        case 2: {
            $("#tooltip_theme").css("visibility", "visible");
            break;
        }
    }
}

function hidetooltip(wich) {
    switch (wich) {
        case 0: {
            $("#tooltip_exit").css("visibility", "hidden");
            break;
        }
        case 1: {
            $("#tooltip_edit_profile").css("visibility", "hidden");
            break;
        }
        case 2: {
            $("#tooltip_theme").css("visibility", "hidden");
            break;
        }

    }
}