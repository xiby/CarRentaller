function $(elementID) {
    return document.getElementById(elementID);
}

function repwblur() {
    var psw = $("wpasw")
    var cpsw = $("Cpsw")
    if (cpsw.value == "") {
        cpsw.className = "error_promopt";
        cpsw.innerHTML = "重复密码不能为空，请重复输入密码";
        return false;
    }
}