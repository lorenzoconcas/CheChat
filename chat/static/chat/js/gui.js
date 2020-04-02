//Questa funzione costruisce l'elemento "bolla" da inserire nelle conversazioni (vale per i messaggi ricevuti dal server=
function getBubble(message) {

    var bubble = document.createElement("div");
    $(bubble).addClass("bubble_container");

    if (message.inviato == "True")
        $(bubble).addClass("outgoing");
    else
        $(bubble).addClass("incoming");

    if (message.mittente != "") {
        var mittente = document.createElement("label")
        $(mittente).text(message.mittente);
        $(mittente).addClass("bubble_sender_name");
        $(bubble).append(mittente);
        $(bubble).append("<br>");
    }


    var msg = document.createElement("label");
    $(msg).text(message.contenuto);
    $(bubble).append(msg);

    return bubble;
}

//queste due funzioni aprono e chiudono un dato pannello passato per riferimento
function closePanel(panel_name) {
    $("#" + panel_name).css("top", "150%");
}
function openPanel(panel_name) {
    if (isMobile)
        $("#" + panel_name).css("top", 0);
    else
        $("#" + panel_name).css("top", "48px");
}

//mostra all'utente i tooltip al passaggio del mouse
function tooltip(wich, visible) {

    status = visible ? "visible" : "hidden";
    $("#" + wich).css("visibility", status);
}

//alterna il tema (chiaro/scuro)
function toggleTheme() {
    if (dark_mode) {
        dark_mode = false;


         $(".thread_title").css("color", "black");
        $(".thread_preview").css("color", "black");
        $(".thread_icon").css("background", "white");
        $(".contact_icon").css("background", "white");
         document.getElementById("themeImg").src = "/static/chat/icons/light_mode.png";
         document.getElementById('theme').href = "/static/chat/css/light.css";
    } else {
        dark_mode = true;

        document.getElementById("themeImg").src = "/static/chat/icons/dark_mode.png";

        $(".thread_title").css("color", "white");
        $(".thread_preview").css("color", "white");
        $(".thread_icon").css("background", "#1a1a1a");
        $(".contact_icon").css("background", "#1a1a1a");
         document.getElementById("theme").href = "/static/chat/css/dark.css";
    }

    setCookie("darkmode", dark_mode, 365*75);

}

//si occupa di aprire il pannello dei contatti, che può essere aperto in modalità rubrica o in modalità nuova chat
function openCECPanel(mode) {
     $("#input_panel_error").css("visibility", "hidden");
    openPanel("chat_and_contacts_panel");
    $("#contacts_search_box").text("");
    if (mode) { //se nuova chat
        $("#cec_title").text("Nuova Chat");
        $("#contacts_list").css("height", "calc(100% - 98px)");
        $("#cec_footer").hide();
        $(".contact_checkbox").show();
        $(".contact_delete").hide();

        $("#cec_startchat").show();
        $("#contacts_search_box").css("visibility", "hidden");
        $("#contacts_search_btn").css("visibility", "hidden");
        $("#contacts_list").css("top", "-24px");


    } else {
        $("#cec_title").text("Rubrica");
        $("#contacts_list").css("height", "calc(100% - 132px)");
        $("#cec_footer").show();
        $(".contact_checkbox").hide();
        $(".contact_delete").show();
        $("#cec_startchat").hide();
         $("#contacts_search_box").css("visibility", "visible");
        $("#contacts_search_btn").css("visibility", "visible");
        if(isMobile)
             $("#contacts_list").css("top", "160px");
        else
             $("#contacts_list").css("top", "10px");
    }
}

//mostra/nasconde il pannello aggiunta contatti
function openInputPanel() {
    $("#input_panel").css("top", "calc(50% - 50px)");

    $("#input_panel").css("height", "100px");
    $("#input_panel_error").hide();
    $("#input_panel_title").text("Nuovo contatto");
    $("#input_panel_text").attr("placeholder", "Inserisci un indirizzo mail");
    $("#input_panel_btn_confirm").on("keypress", addContact2);
    $("#input_panel_btn_confirm").click(addContact);
}
function hideInputPanel(){
    $("#input_panel").css("height", "100px");
    $("#input_panel_error").show();
    $("#input_panel_error").css("visibility", "hidden");
    $("#input_panel_error").text("");
}

//restituisce l'elemento da aggiungere nella barra laterale delle chat
function getThreadItem(chat_name, id, icon_path) {

    let div = document.createElement("div");
    let img = document.createElement("img");
    let name = document.createElement("label");
    let status = document.createElement("label");
    let preview = document.createElement("label");

    $(div).addClass("chat_thread");

    img.id = "thread_icon_"+id;
    img.src = icon_path;
    $(img).addClass("thread_icon")
    $(name).text(chat_name);

    if (chat_name.length > 28){
        $(name).text(chat_name.substring(0, 28) + '...');
        $(name).css("font-size", "16px");
    }

    $(name).addClass("thread_title");
    $(status).addClass("thread_status");
    $(preview).addClass("thread_preview");
    $(name).attr("id", "thread_title_" + id);
    $(status).attr("id", "thread_status_" + id);
    $(status).text("")
    $(preview).addClass("id", "thread_preview_" + id);

    $(div).append(img);
    $(div).append(name);
    $(div).append(status);
    $(div).append("<br>");
    $(div).append(preview);


    $(div).attr("id", "thread_" + id);
    $(div).attr("onclick", "openThread(" + id + ")");
    return div
}
//nasconde la chat
function closeChatThread() {
    if (isMobile) {
        $("#chat").css("left", "100%");
        $("#new_thread").css("visibility", "visible");
        $("#new_thread").toggle(250);
        $(".chat_thread").css("background", "transparent");
        $("#thread_bubbles").empty();

    }
      currentChat = 0;
}

//usato dall'app mobile (opzionale)
function injectNativeAppCSS(){
    let file = "/static/chat/css/mobile_native.css"

    let link = document.createElement( "link" );
    link.href = file;
    link.type = "text/css";
    link.rel = "stylesheet";
    link.media = "screen,print";

    document.getElementsByTagName( "head" )[0].appendChild( link );
}

function addBubble(msg){
    let divElement;
    let child_count = $("#thread_bubbles").children().length;

    if (child_count === 0) {
        $("#thread_bubbles").append("<br>");
        $("#thread_bubbles").append("<br>");
        $("#thread_bubbles").append("<br>");
    }

    divElement = getBubble(msg);
    $("#thread_bubbles").append(divElement).append("<br>");

    let curHeight = $(divElement).css("height");
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
}