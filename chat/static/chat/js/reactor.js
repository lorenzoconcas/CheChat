function onFieldInput(){
    var userNField = document.getElementById("email_field");
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
function onFieldRegisterInput() {
    var userNField = document.getElementById("name_field");
    var surnameField = document.getElementById("surname_field");
    var emailField = document.getElementById("email_field");
    var pswdField = document.getElementById("password_field");
    var confPswdField = document.getElementById("confirm_password_field");
    var loginBtn = document.getElementById("login_btn");


    var uFilled = userNField.value !== '';
    var pFilled = pswdField.value !== '';
    var sFilled = surnameField.value !== '';
    var eFilled = emailField.value !== '';
    var cPFilled = confPswdField.value !== '';

     if(uFilled && pFilled && sFilled && eFilled && cPFilled){
        loginBtn.style.backgroundColor = "#0099FF";
        loginBtn.style.color = "white";
    }else{
        loginBtn.style.backgroundColor = "rgba(232,232,232,0.8)";
        loginBtn.style.color = "";
    }
}