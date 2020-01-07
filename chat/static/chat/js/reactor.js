function onFieldInput(){
    var userNField = document.getElementById("username_field");
    var pswdField = document.getElementById("password_field");
    var loginBtn = document.getElementById("login_btn");

    var uFilled = userNField.value !== '';
    var pFilled = pswdField.value !== '';

    if(uFilled && pFilled){
        loginBtn.style.backgroundColor = "#0099FF";
        loginBtn.style.color = "white";
    }else{
        loginBtn.style.backgroundColor = "rgba(232,232,232,0.8)";
        loginBtn.style.color = "";
    }


}
