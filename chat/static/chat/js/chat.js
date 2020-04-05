let isMobile = false;
let dark_mode = false;
let currentChat = 0;
let unreaded_messages = 0;
let adding_partecipant = false;
let open_new_thread = false;
function setup() {
    //calcolo se ci troviamo su un dispositivo mobile o a vista singola
    isMobile = detectMobile();//$("#user_name").css("visibility") == "hidden" ? true : false;

    if(isMobile)
         loadMobileCSS();

    $("#chat_title").text($("#chat_thread_1").text());
   
    var x = document.cookie;
    dark_mode = getCookie("darkmode");
    toggleTheme();

    putAllIcons();

}
function loadMobileCSS(){
	  var head = document.getElementsByTagName('head')[0];
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = 'static/chat/css/mobile.css';
        link.media = 'all';
        head.appendChild(link);
}
function detectMobile() {
    return (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino|android|ipad|playbook|silk/i.test(navigator.userAgent || navigator.vendor || window.opera) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test((navigator.userAgent || navigator.vendor || window.opera).substr(0, 4)))
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

function sendMessage() {
    let msg = document.getElementById("message_box");
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
               // console.log(data)
            },
        });
        /*
         "type": "new_message","chat_id": "ultimo.chat.id,""mittente": "", "contenuto", "inviato":  "True"
        * */
        let bubble = JSON.parse('[{"type": "new_message", "mittente": "", "contenuto" : "'+ msg.value +'", "inviato":"True"}]');
        addBubble(bubble[0]);
         $("#thread_preview_"+currentChat).text("Tu: "+msg.value.substring(0, 20));
        msg.value = '';
        $("#thread_"+currentChat).prependTo("#thread_list");
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
        if(!dark_mode){
             $(".thread_title").css("color", "black");
             $(".thread_preview").css("color", "black");
        }


        $("#thread_" + chat_id).css("background", "dodgerblue");
        $("#thread_title_" + chat_id).css("color", "white");
        $("#thread_preview_" + chat_id).css("color", "white");
    }
     $("#chat_title").text($("#thread_title_" + chat_id).text());
    currentChat = chat_id;

    let size = notifications.length;
    for (let i = 0; i < size; i++) {
        let n = notifications[i];
        if (n.thread_id === chat_id) {
            let actual_title = $("#thread_title_" + n.thread_id).text()
            let new_thread_title = actual_title.replace('- (' + n.notification_count + ')')
            $("#thread_title_" + n.thread_id).text(new_thread_title);
            unreaded_messages = unreaded_messages - n.notification_count;
            n.notification_count = 0;
        }
    }
    //chat_user_icon
    //
    document.getElementById("chat_user_icon").src = $("#thread_icon_"+currentChat).attr("src");
    unreaded_messages > 0 ? document.title = "Nuovo messaggio (" + unreaded_messages + ")" : document.title = "ISW Chat"
    $("#thread_bubbles").empty();
    $("#chat").append("<br>");
    $("#chat").append("<br>");
    $("#chat").append("<br>");
    $("#chat").append("<br>");
    $("#chat").css("visibility", "visible");
    loadMessages(chat_id);
}
function loadMessages(chat_id) {
    $.ajax({
        type: "POST",
         url: "client_reqs/",
        data: {
            'req' : 'get_all_messages',
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
    let mail = $("#contacts_search_box").val();
    if(mail === "")
        return;
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
                let del_img = document.createElement("img");


                $(del_img).addClass("contact_delete_icon");
                del_img.src = "/static/chat/icons/remove_contact.png"

                $(div).addClass("contact_element");
                $(checkbox).addClass("contact_checkbox");
                $(checkbox).attr("id", data[0].id);
                let img_id =  parseInt(data[0].id % 5);
                let img_src = "/static/chat/icons/user_icon_"+ img_id +".png"
                $(img).attr("src", img_src );
                $(img).addClass("contact_icon")
                $(name).text(data[0].name);
                $(name).addClass("contact_name");
                $(del_btn).addClass("contact_delete");
                $(del_btn).append(del_img);

                $(div).append(checkbox);
                $(checkbox).hide();
                $(div).append(img);
                $(div).append(name);
                $(div).append(del_btn);

                $(div).attr("id", "contact_"+data[0].id);
                $("#contacts_list").append(div);
                  if($("#contacts_list").css("top") !== "10px")
                    $("#contacts_list").css("top", "10px");
            }
            else{
                //<label id="input_panel_error">Errore</label>
                $("#input_panel").css("height", "120px");
                $("#input_panel_error").show();
                $("#input_panel_error").css("visibility", "visible");
                $("#input_panel_error").text(data[0].error);
                if($("#contacts_list").css("top") !== "32px")
                    $("#contacts_list").css("top", "32px");
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
                'starting_thread' : adding_partecipant,
                'base_thread': currentChat,
            },

            beforeSend: function (request, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    request.setRequestHeader("X-CSRFToken", csrfcookie());
                }
            },
            dataType: 'json',
            success: function (data) {

                if (data[0].result == "ok") {
                    closePanel("chat_and_contacts_panel");
                     let icon = data[0].icon;
                     let chat_name =  data[0].chat_name;
                     let chat_id = data[0].id;
                    let new_thread_div = getThreadItem(chat_name, chat_id, icon)

                    $("#thread_list").prepend(new_thread_div);
                     openThread(chat_id);


                }
            }
        });
    }
    adding_partecipant = false;
}

function deleteChat(){
    console.log("Deleting chat "+currentChat);
    if(currentChat === 0)
        return;

     $.ajax({
        type: "POST",
          url: "client_reqs/",
        data: {
            'req' : 'delete_chat',
            'chat_id': currentChat,
        },

        beforeSend: function(request, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                request.setRequestHeader("X-CSRFToken", csrfcookie());
            }
        }, dataType: 'json',
        success: function(data) {
            console.log(data);
            if(data[0].delete === "ok"){
                $("#thread_"+currentChat).remove();
                closeChatThread();
                $("#chat").css("visibility", "hidden");
            }
        },
    });
}

function addPartecipant() {
    adding_partecipant = true;
    openCECPanel(1);
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function setChatIcon(threadID){
     let icon = document.getElementById("thread_icon_"+threadID);
     $.ajax({
            type: "POST",
              url: "client_reqs/",
            data: {
               'req': 'get_chat_icon',
               'chat_id': threadID,
            },

            beforeSend: function (request, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    request.setRequestHeader("X-CSRFToken", csrfcookie());
                }
            },
            success: function (data) {

                icon.src = data;
            },
            error: function () {
                icon.src =   'static/chat/icons/user_group.png'
            }
     });
}

function setContactIcon(userID){
     let icon = document.getElementById("contact_icon_"+userID);
     let icon_id = parseInt(userID % 5);
     icon_id = icon_id == 0 ?  1 : icon_id;
     icon.src = 'static/chat/icons/user_icon_'+icon_id+'.png'

}


function putAllIcons(){

     $(".chat_thread").each(function (index) {
        let id = $(this).attr('id');
        id = id.replace("thread_", "");
        setChatIcon(id);
    })
    $(".contact_icon").each(function (index) {
        let id = $(this).attr('id');
        id = id.replace("contact_icon_", "");
        setContactIcon(id);
    })
}