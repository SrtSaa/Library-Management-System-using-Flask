function validateSearch() {
    var returnval = true;
    var s = document.forms['search']["q"].value;
    if (s.length == 0) {
        returnval = false;
    }
    s = s.trim()
    if (s.length == 0) {
        returnval = false;
    }
    return returnval;
}