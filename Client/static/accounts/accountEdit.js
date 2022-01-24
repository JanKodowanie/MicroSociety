var usernameReg = new RegExp("^[a-zA-Z0-9]{6,20}$")
var usernameMessage = "Nazwa użytkownika musi składać się z 6-20 znaków alfanumerycznych."

var dataForm = null
var pictureForm = null

var fieldState = {
    "username": true,
}

window.addEventListener("load", initialize, true); 

function initialize() {
    dataForm = document.getElementById("account-edit-form")
    pictureForm = document.getElementById("picture-form")
    
    dataForm.addEventListener("submit", onSubmitData)
    pictureForm.addEventListener("submit", onSubmitPicture)

    document.getElementById("username").addEventListener("change", validateUsername)
    document.getElementById("picture-delete").addEventListener("click", onDeletePicture)
} 

validateUsername = function () {
    var username = document.getElementById("username").value
    var errorMsg = document.getElementById("username-error")

    if (usernameReg.test(username)) {
        errorMsg.className = "error-mes-hidden"
        errorMsg.innerText = ""
        fieldState['username'] = true
                    
    } else {
        fieldState['login'] = false
        errorMsg.className = "error-mes"
        errorMsg.innerText = usernameMessage
    }
}

onSubmitData = async function (e) {
    e.preventDefault()
    var valid = true
    var usernameErrorMsg = document.getElementById("username-error")
    var emailErrorMsg = document.getElementById("email-error")

    if (!fieldState["username"]) {
        valid = false
        usernameErrorMsg.className = "error-mes"
        usernameErrorMsg.innerText = usernameMessage
    }
    
    if (valid) {
        let data = new FormData(dataForm)
        let value = Object.fromEntries(data.entries())
        let response = await fetch('/account', {method: 'PUT', headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }, body: JSON.stringify(value)})
        let response_data = await response.json()
        if (response.status === 422) {
            if (response_data.detail && response_data.detail.username) {
                usernameErrorMsg.className = "error-mes"
                usernameErrorMsg.innerText = response_data.detail.username
            }
            if (response_data.detail && response_data.detail.email) {
                emailErrorMsg.className = "error-mes"
                emailErrorMsg.innerText = response_data.detail.email
            }
        } else {
            var msg = document.getElementById("success-mes")
            msg.className = "error-mes"
            msg.innerText = response_data.detail
            msg.style.color = "#008000"
        }
    }    
}

onSubmitPicture = async function (e) {
    e.preventDefault()
    var pictureErrorMsg = document.getElementById("picture-error")
    let data = new FormData(pictureForm)
    let response = await fetch('/account/profile-picture', {method: 'PATCH', body: data})
    let response_data = await response.json()

    if (response.status === 422) {
        if (response_data.detail) {
            pictureErrorMsg.className = "error-mes"
            pictureErrorMsg.innerText = response_data.detail
        }
    } else {
        window.location.reload()
    }
}    

onDeletePicture = async function (e) {
    e.preventDefault()
    var pictureErrorMsg = document.getElementById("picture-error")
    let response = await fetch('/account/profile-picture', {method: 'DELETE'})
    let response_data = await response.json()

    if (response.status !== 200) {
        if (response_data.detail) {
            pictureErrorMsg.className = "error-mes"
            pictureErrorMsg.innerText = response_data.detail
        }
    } else {
        window.location.reload()
    }
}    