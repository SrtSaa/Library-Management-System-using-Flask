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

function validateBookinfo(){
    var returnval = true;
    clearErrors();

    var isbn = document.forms['form']["fisbn"].value;
    if(isbn.length!=10 && isbn.length!=13){
        seterror("isbn","*Enter Valid ISBN Number!");
        returnval = false;
    }

    var s = document.forms['form']["ftitle"].value;
    s = s.trim()
    if (s.length==0) {
        seterror("title","*Title cannot be empty");
        returnval = false;
    }
    
    var s = document.forms['form']["fpub"].value;
    s = s.trim()
    if (s.length==0) {
        seterror("pub","*Publisher cannot be empty");
        returnval = false;
    }

    var y = document.forms['form']["fyear"].value;
    var d = new Date();
    var cy = d.getFullYear();
    if(y>parseInt(cy)){
        seterror("year","*Enter Valid Year!");
        returnval = false;
    }
    else if(y<1990){
        seterror("year","*Year must be greater or equal 1990!");
        returnval = false;
    }

    var s = document.forms['form']["ffau"].value;
    s = s.trim()
    if (s.length==0) {
        seterror("fau","*First Author cannot be empty");
        returnval = false;
    }

    var c = document.forms['form']["fcp"].value;
    if(c>26){
        seterror("cp","*For now, a book can have atmost 26 copies!");
        returnval = false;
    }
    return returnval;
}