let notification_sound = new Audio('/static/chat/audio/notify.ogg');
//oggetto notifica
const notification = {
    thread_id: 0,
    notification_count: 0
};
//contenitore notifiche
let notifications = [];

//il websocket che si occuperà di ricevere i dati dal server in caso di nuovi messaggi
let push_socket = new WebSocket("ws://" + window.location.host + "/ws/push_messages");
//alla connessione comunichiamo al server di essere pronti a ricevere nuovi messaggi
push_socket.onopen = function() {
    askForMessages();
};
//qui gestiamo i dati ricevuti
push_socket.onmessage = function(e) {
    let n;
    let msg = JSON.parse(e.data)
    console.log("new data from ws "+msg);
    switch(msg.type){
        case 'new_chat':{

            $("#thread_list").append(getThreadItem(msg.name, msg.id));
            break;
        }
        case 'new_message': {
            $("#thread_preview_" + msg.chat_id).text(msg.contenuto)
            $("#thread_status_" + msg.chat_id).text("");

            notification_sound.play();


            let divElement;
            if (currentChat == msg.chat_id) {
                divElement = getBubble(msg);
                $("#thread_bubbles").append(divElement).append("<br>");

                var curHeight = $(divElement).css("height");
                $(divElement).css("height", "0");
                $(divElement).css("width", "0");
                $("#thread_bubbles").animate({
                    scrollTop: $('#thread_bubbles').prop("scrollHeight")
                }, 1000);
                $(divElement).animate({
                    width: "45%",
                    height: $(divElement).get(0).scrollHeight
                }, 250, function () {
                    $(this).height('auto');
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
                        new_thread_title = $("#thread_title_" + n.thread_id).text().replace("(" + n.notification_count - 1 + ")") + " (" + n.notification_count + ")"

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

//comunica al server di essere pronto a ricevere messaggi
function askForMessages() {
    let message = JSON.stringify({
        'ready': 'True'
    })
    push_socket.send(message);
}