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
push_socket.onclose = function(){
    push_socket = new WebSocket("ws://" + window.location.host + "/ws/push_messages");
};

//qui gestiamo i dati ricevuti

push_socket.onmessage = function(e) {
    let n;

    let msg = JSON.parse(e.data);
    console.log(msg);
    switch(msg.type){
        case 'new_chat':{
            console.log("nuova chat");
            notification_sound.play();
            let icon = msg.thread_icon;

            let new_thread_div = getThreadItem(msg.name, msg.id, icon)

            $("#thread_list").prepend(new_thread_div);

        }
        case 'new_message': {
            console.log("nuovo msg");
            $("#thread_preview_" + msg.chat_id).text(msg.content)
            $("#thread_status_" + msg.chat_id).text("");
            if(msg.inviato === false){
                notification_sound.play();
            }


            if (currentChat === msg.chat_id) {
                addBubble(msg);
            } else {

                let new_thread_title = "";
                unreaded_messages++;
                if (notifications.length === 0) {
                    n = Object.create(notification);
                    n.thread_id = msg.chat_id;
                    n.notification_count++;
                    notifications.push(n);
                    new_thread_title = $("#thread_title_" + msg.chat_id).text() + " (1)"

                } else {
                    let size = notifications.length;

                    for (let i = 0; i < size; i++) {
                        n = notifications[i];
                        if (n.thread_id === msg.chat_id)
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