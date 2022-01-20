var newPass1Reg = new RegExp("^.{6,30}$")
var newPassMessage = "Hasło musi zawierać przynajmniej 6 znaków. Maksymalna długość hasła to 30 znaków."
var newPass2Message = "Hasła nie są zgodne."
var passForm = null

var fieldState = {
    "newPass1": false,
    "newPass2": false
}


window.addEventListener("load", initialize, true); 

function initialize() {
    passForm = document.getElementById("password-change")
    passForm.addEventListener("submit", onSubmitData)
    document.getElementById("new-pass1").addEventListener("change", validateNewPass1)
    document.getElementById("new-pass2").addEventListener("change", validateNewPass2)
} 

validateNewPass1 = function () {
    let password = document.getElementById("new-pass1").value
    let errorMsg = document.getElementById("new-pass1-error")

    if (newPass1Reg.test(password)) {
        fieldState["newPass1"] = true
        errorMsg.className = "error-mes-hidden"
        errorMsg.innerText = ""
    } else {
        fieldState["newPass1"] = false
        errorMsg.className = "error-mes"
        errorMsg.innerText = newPassMessage
    }
}

validateNewPass2 = function () {
    let password = document.getElementById("new-pass1").value
    let password2 = document.getElementById("new-pass2").value
    let errorMsg = document.getElementById("new-pass2-error")

    if (password !== "" && password !== password2) {
        fieldState["newPass2"] = false
        errorMsg.className = "error-mes"
        errorMsg.innerText = newPass2Message
    } else if (password !== "") {
        fieldState["newPass2"] = true
        errorMsg.className = "error-mes-hidden"
        errorMsg.innerText = ""
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


onSubmitData = async function (e) {
    e.preventDefault()
    var valid = true

    if (!fieldState["newPass1"]) {
        valid = false       
        validateNewPass1()
    }
    if (!fieldState["newPass2"]) {
        valid = false
        validateNewPass2()
    }
    
    if (valid) {
        let data = new FormData(e.target)
        let msg = document.getElementById("pass-message")
        
        let response = await fetch(window.location.href, {method: 'PATCH', body: data})
        response_data = await response.json()

        if (response.status === 200) {
            msg.className = "error-mes"
            msg.innerText = response_data.detail
            msg.style.color = "#008000"
            await sleep(1200)
            window.location.href = "/login"
        } else {
            msg.className = "error-mes"
            msg.innerText = response_data.detail
        }
    }    
}