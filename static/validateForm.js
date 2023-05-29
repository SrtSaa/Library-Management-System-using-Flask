function clearErrors() {
    errors = document.getElementsByClassName('formerror');
    for (let item of errors) {
        item.innerHTML = "";
    }
}



function seterror(id, error) {
    element = document.getElementById(id);
    element.getElementsByClassName('formerror')[0].innerHTML = error;
}



function validateEmail() {
    var returnval = true;

    var email = document.forms['form']["femail"].value;
    if (email.length > 30) {
        seterror("email", "*Email length is too long<br>");
        returnval = false;
    }
    return returnval;
}

function validateEmail2() {
    var returnval = true;

    var email = document.forms['form2']["femail"].value;
    if (email.length > 30) {
        seterror("email2", "*Email length is too long<br>");
        returnval = false;
    }
    return returnval;
}



function validatePassword() {
    var returnval = true;
    var password = document.forms['form']["fpass"].value;
    if (password.length < 8) {
        seterror("pass", "*Password should be atleast 8 characters long!<br>");
        returnval = false;
    }
    else if (password.length > 15) {
        seterror("pass", "*Password should be atmost 15 characters long!<br>");
        returnval = false;
    }
    else {
        if (!password.match(/[a-z]/g) || !password.match(/[A-Z]/g)
            || !password.match(/[0-9]/g) || !password.match(/[^a-zA-Z\d]/g)) {
            seterror("pass", "*Passsword must contain atleast 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character!<br>");
            returnval = false;
        }
    }

    return returnval;
}

function validatePassword2() {
    var returnval = true;
    var password = document.forms['form2']["fpass"].value;
    if (password.length < 8) {
        seterror("pass2", "*Password should be atleast 8 characters long!<br>");
        returnval = false;
    }
    else if (password.length > 15) {
        seterror("pass2", "*Password should be atmost 15 characters long!<br>");
        returnval = false;
    }
    else {
        if (!password.match(/[a-z]/g) || !password.match(/[A-Z]/g)
            || !password.match(/[0-9]/g) || !password.match(/[^a-zA-Z\d]/g)) {
            seterror("pass2", "*Passsword must contain atleast 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character!<br>");
            returnval = false;
        }
    }

    return returnval;
}



function validateConfirmPassword() {
    var returnval = true;
    var p = document.forms['form']["fpass"].value;
    var cp = document.forms['form']["fcpass"].value;
    if (p != cp) {
        seterror("fcpass", "*Password and Confirm Password must be same!<br>");
        returnval = false;
    }

    return returnval;
}



function validateForm(){
    var returnval = true;
    clearErrors();
    returnval = validateEmail();
    if (returnval == false) {
        return returnval;
    }
    returnval = validatePassword();
    return returnval;
}


function validateForm2(){
    var returnval = true;
    clearErrors();
    returnval = validateEmail2();
    if (returnval == false) {
        return returnval;
    }
    returnval = validatePassword2();
    return returnval;
}


function validateForm3(){
    var returnval = true;
    clearErrors();
    returnval = validateEmail();
    if (returnval == false) {
        return returnval;
    }
    returnval = validatePassword();
    if (returnval == false) {
        return returnval;
    }
    returnval = validateConfirmPassword();
    return returnval;
}