var isMobile = false;
var dark_mode = false;
var currentChat = 1;

function getfirstchatid(){

}
function funcs() {
    var x = document.getElementById("thread_bubbles")
    x.scrollTo(0,x.scrollHeight);
     var el = document.getElementById('navbar_title');
    var style = window.getComputedStyle(el, null).getPropertyValue('font-size');
    var fontSize = parseFloat(style);
    isMobile = fontSize >= 80 ? true : false;
   // toggleTheme();

    $("#chat_title").text($("#chat_thread_1").text())

   // checkMessages();
}

function fromServer(){
  return new Promise((resolve, reject) => {
        let lastmsg = "";
   $.ajax({
       type: "POST",
       url: "/lastmessage/",
       data:{
           'chat_id': currentChat
       },
       beforeSend: function(request, settings) {
           if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
               request.setRequestHeader("X-CSRFToken", csrfcookie());
           }},
        success:function(data){


           resolve(data);
        }
    });
  })
}

async function checkMessages(){
    let lastmsg = "";
    while (true) {
      let x =  await fromServer();
      if(x != lastmsg && x != "" && !elementAlreadyInserted(x)){
          lastmsg = x
          var divElement = document.createElement("div");
          $(divElement).addClass("bubble_container");
          $(divElement).addClass("incoming");
          var msg = document.createElement("label");
          $(msg).text(x);
          $(divElement).append(msg);
          $("#thread_bubbles").append(divElement).append("<br>");
          $(divElement).css("width", "0");
          var curHeight = $(divElement).css("height");

          $(divElement).css("height", "0");
          $(".lastElement").removeClass("lastElement");
          $(msg).addClass("lastElement");
          $("#thread_bubbles").animate({ scrollTop: $('#thread_bubbles').prop("scrollHeight")}, 1000);
          $(divElement).animate({width: "45%", height: curHeight}, 250, function(){} );
      }
      console.log(x==lastmsg);
    }
}

function elementAlreadyInserted(msg){
    return $(".lastElement").text() == msg;
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


function sendMessage(){
    var msg = document.getElementById("message_box");
    if(msg.value !== ''){
         $.ajax(
        {
            type: "POST",
            url: "/sendmessage/",
            data:{
                'msg': msg.value,
                'chat_id': 1
            },
              beforeSend: function(request, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                            request.setRequestHeader("X-CSRFToken", csrfcookie());
                        }
                    },
            success: function( data )
            {
                console.log(data)

            },
         });




        var br = document.createElement("br");
        var msg_text = document.createElement("label");
        msg_text.textContent = msg.value;
        var msg_bubble = document.createElement("div");

        msg_bubble.appendChild(msg_text);

        var target = document.getElementById("thread_bubbles");

        var bubble_clone = $(msg_bubble).clone();
        $(bubble_clone).addClass("bubble_container");
            $(bubble_clone).addClass("outgoing");
            $(bubble_clone).css("opacity", "0");
            $(bubble_clone).appendTo(target);
             target.appendChild(br).scrollIntoView(true);

             $(msg_bubble).addClass("moving_bubble");

        $("#send_box").append(msg_bubble);

        var bcW = $(bubble_clone).css("width");
        console.log(bcW);
       $(msg_bubble).animate( {
            top: "-42px",
            left: "52%",
            width:  "-=240px",
            height: "-=6px",

          }, 250, "linear", function() {


            $(bubble_clone).animate(
                {
                    opacity: 1,
                },
                250,
                "linear",
                function(){
                    $(msg_bubble).fadeTo(350, 0);

                    target.appendChild(br).scrollIntoView(true);
                    $(msg_bubble).remove();
                }
            )
          });

         msg.value = '';
    }
}

function sendMessageOnEnter(e){
    if(e.keyCode === 13){
         var msg = document.getElementById("message_box");
        e.preventDefault();
           sendMessage();

    }
    // user: '{{ user }}'
}

function closeNewChat(){
    $("#new_chat_panel").css("top", "150%");

}
function openNewChat() {
    if(isMobile)
        $("#new_chat_panel").css("top", "128px");
    else
        $("#new_chat_panel").css("top", "25%");
}
function openThread(chat_id) {
    if(isMobile) {
        $("#chat").css("left", "0");
        $("#new_thread").css("visibility", "hidden");

    }
    currentChat = chat_id;
    $("#chat_title").text($("#chat_thread_"+chat_id).text());
    $("#chat").css("visibility", "visible");
    loadMessages(chat_id);

}

function loadMessages(chat_id){
      $.ajax(
        {
            type: "POST",
            url: "/allmessages/",
            data:{
                'chat_id': chat_id
            },
              beforeSend: function(request, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                            request.setRequestHeader("X-CSRFToken", csrfcookie());
                        }
                    },
             dataType: 'json',
            success: function( data )
            {
                console.log(data)

                $("#thread_bubbles").empty();
                $("#thread_bubbles").append("<br>");
                $("#thread_bubbles").append("<br>");
                $("#thread_bubbles").append("<br>");
                for(var messaggio in data){
                    $("#thread_bubbles").append(getBubble(data[messaggio]));
                     $("#thread_bubbles").append("<br>");
                }

            },
         });
}

function getBubble(messaggio){
       var bubble = document.createElement("div");
       $(bubble).addClass("bubble_container");

        if(messaggio.inviato == "True")
             $(bubble).addClass("outgoing");
        else
          $(bubble).addClass("incoming");

        var msg = document.createElement("label");
          $(msg).text(messaggio.contenuto);
          $(bubble).append(msg);

          console.log(messaggio.contenuto);
         return bubble;
}
function openChatThreadDetail() {
    alert("to do");
}
function toggleTheme() {

    if(dark_mode) {
        dark_mode = false;
        document.getElementById('theme').href = "/static/chat/css/light.css";
         document.getElementById("theme_mode_btn").innerText = "";
    }
    else {
        dark_mode = true;
        document.getElementById("theme").href = "/static/chat/css/dark.css";
        document.getElementById("theme_mode_btn").innerText = "";
    }
}

function showtooltip(wich) {
    switch(wich){
        case 0:{
            $("#tooltip_exit").css("visibility", "visible");
            break;
        }
          case 1:{
             $("#tooltip_edit_profile").css("visibility", "visible");
             break;
        }

        case 2:{
             $("#tooltip_theme").css("visibility", "visible");
             break;
        }
    }
}
function hidetooltip(wich) {
    switch(wich){
        case 0:{
            $("#tooltip_exit").css("visibility", "hidden");
            break;
        }
        case 1:{
             $("#tooltip_edit_profile").css("visibility", "hidden");
             break;
        }
        case 2:{
             $("#tooltip_theme").css("visibility", "hidden");
             break;
        }

    }
}