var isMobile = false;
var dark_mode = false;
function funcs() {
    var x = document.getElementById("thread_bubbles")
    x.scrollTo(0,x.scrollHeight);
     var el = document.getElementById('navbar_title');
    var style = window.getComputedStyle(el, null).getPropertyValue('font-size');
    var fontSize = parseFloat(style);
    isMobile = fontSize >= 80 ? true : false;
   // toggleTheme();
}
function sendMessage(){
    var msg = document.getElementById("message_box");
    if(msg.value !== ''){
        var br = document.createElement("br");
        var msg_text = document.createElement("label");
        msg_text.textContent = msg.value;
        var msg_bubble = document.createElement("div");

        msg_bubble.appendChild(msg_text);

        var target = document.getElementById("thread_bubbles");

      /* $(msg_bubble).css("position", "absolute");
        $(msg_bubble).css("left", "8px");
        $(msg_bubble).css("z-index", "17");
        $(msg_bubble).css("top", "calc(50% - 22px)");
        $(msg_bubble).css("height", "24px");
        $(msg_bubble).css("width", "calc(100% - 124px)");
        $(msg_bubble).css("color", "white");
        $(msg_bubble).css("background", "dodgerblue");
        $(msg_bubble).css("border-radius", " 32px");
        $(msg_bubble).css("padding", "8px 16px");
        $(msg_bubble).css("border-style", "solid");*/



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
        e.preventDefault();
        sendMessage();
    }
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
function openThread() {
    if(isMobile) {
        $("#chat").css("left", "0");
        $("#new_thread").css("visibility", "hidden");
        window.location.hash("#chat")
    }
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