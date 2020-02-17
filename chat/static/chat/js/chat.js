var isMobile = false;
var dark_mode = false;
function funcs() {
    var x = document.getElementById("thread_bubbles")
    x.scrollTo(0,x.scrollHeight);
     var el = document.getElementById('navbar_title');
    var style = window.getComputedStyle(el, null).getPropertyValue('font-size');
    var fontSize = parseFloat(style);
    isMobile = fontSize >= 80 ? true : false;
    toggleTheme();
}
function sendMessage(){
    var msg = document.getElementById("message_box");
    if(msg.value !== ''){
        var br = document.createElement("br");
        var tNode = document.createElement("label");
        tNode.textContent = msg.value;
        var x = document.createElement("div");
        x.classList.add("bubble_container");
        x.classList.add("outgoing");
        x.appendChild(tNode);
        var target = document.getElementById("thread_bubbles");
        target.appendChild(x);
        target.appendChild(br).scrollIntoView(true)
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

