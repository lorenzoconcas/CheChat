function funcs() {
    var x = document.getElementById("thread_bubbles")
    x.scrollTo(0,x.scrollHeight);
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