function seterror(id, error) {
    element = document.getElementById(id);
    element.getElementsByClassName('formerror')[0].innerHTML = error;
}

function validateBcpy(){
    var returnval = true;

    var c = parseInt(document.forms['form']["cpy"].value);
    var a = parseInt(document.forms['form']["fcp"].value);
    console.log(c)
    console.log(a)
    if(c+a>26){
        console.log("true")
        seterror("cp","*For now, a book can have atmost 26 copies!");
        returnval = false;
    }
    return returnval;
}