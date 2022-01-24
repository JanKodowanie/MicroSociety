var passReg = new RegExp("^.{6,30}$")
var usernameReg = new RegExp("^[a-zA-Z0-9]{6,20}$")
var usernameMessage = "Nazwa użytkownika musi składać się z 6-20 znaków alfanumerycznych."
var passwordMessage = "Hasło musi zawierać przynajmniej 6 znaków. Maksymalna długość hasła to 30 znaków."
var password2Message = "Hasła nie są zgodne."
var genderMessage = "Należy wybrać płeć."
var regForm = null


var fieldState = {
    "username": false,
    "password": false,
    "password2": false,
    "gender": false
}

window.addEventListener("load", initialize, true); 

function initialize() {
    regForm = document.getElementById("regform")
    regForm.addEventListener("submit", onSubmitData)

    document.getElementById("username").addEventListener("change", validateUsername)
    document.getElementById("password").addEventListener("change", validatePassword)
    document.getElementById("password2").addEventListener("change", validatePassword2)
    document.getElementById("gender").addEventListener("change", validateGender)
} 


validateUsername = function () {
    var username = document.getElementById("username").value
    var errorMsg = document.getElementById("username-error")

    if (usernameReg.test(username)) {
        errorMsg.className = "error-mes-hidden"
        errorMsg.innerText = ""
        fieldState['username'] = true
                    
    } else {
        fieldState['username'] = false
        errorMsg.className = "error-mes"
        errorMsg.innerText = usernameMessage
    }
}

validatePassword = function () {
    var password = document.getElementById("password").value
    var errorMsg = document.getElementById("password-error")

    if (passReg.test(password)) {
        fieldState['password'] = true
        errorMsg.className = "error-mes-hidden"
        errorMsg.innerText = ""
    } else {
        fieldState['password'] = false
        errorMsg.className = "error-mes"
        errorMsg.innerText = passwordMessage
    }
}

validatePassword2 = function () {
    var password = document.getElementById("password").value
    var password2 = document.getElementById("password2").value
    var errorMsg = document.getElementById("password2-error")

    if (password !== "" && password !== password2) {
        fieldState['password2'] = false
        errorMsg.className = "error-mes"
        errorMsg.innerText = password2Message
    } else if (password !== "") {
        fieldState['password2'] = true
        errorMsg.className = "error-mes-hidden"
        errorMsg.innerText = ""
    }
}

validateGender = function () {
    var gender = document.getElementById("gender").value
    var errorMsg = document.getElementById("gender-error")

    if (gender === "none") {
        fieldState['gender'] = false
        errorMsg.className = "error-mes"
        errorMsg.innerText = genderMessage
    } else {
        fieldState['gender'] = true
        errorMsg.className = "error-mes-hidden"
        errorMsg.innerText = ""
    }
}


onSubmitData = async function (e) {
    e.preventDefault()
    var valid = true
    var usernameErrorMsg = document.getElementById("username-error")
    var emailErrorMsg = document.getElementById("email-error")
    var passwordErrorMsg = document.getElementById("password-error")
    var password2ErrorMsg = document.getElementById("password2-error")
    var genderErrorMsg = document.getElementById("gender-error")

    if (!fieldState["username"]) {
        valid = false
        usernameErrorMsg.className = "error-mes"
        usernameErrorMsg.innerText = usernameMessage
    }
    if (!fieldState["password"]) {
        valid = false       
        passwordErrorMsg.className = "error-mes"
        passwordErrorMsg.innerText = passwordMessage
    }
    if (!fieldState["password2"]) {
        valid = false
        password2ErrorMsg.className = "error-mes"
        password2ErrorMsg.innerText = password2Message
    }
    if (!fieldState["gender"]) {
        valid = false
        genderErrorMsg.className = "error-mes"
        genderErrorMsg.innerText = genderMessage
    }
    
    if (valid) {
        let data = new FormData(regForm)
        let response = await fetch('/sign-up', {method: 'POST', body: data})

        if (response.status === 422) {
            data = await response.json()
            if (data.detail && data.detail.username) {
                usernameErrorMsg.className = "error-mes"
                usernameErrorMsg.innerText = data.detail.username
            }
            if (data.detail && data.detail.email) {
                emailErrorMsg.className = "error-mes"
                emailErrorMsg.innerText = data.detail.email
            }
        } else {
            window.location.href = "/login"
        }
    }    
}