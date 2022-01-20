var errorMsg = null
var loginForm = null

window.addEventListener("load", initialize, true); 

function initialize() {
    loginForm = document.getElementById("loginform")
    loginForm.addEventListener("submit", onSubmitData)
    errorMsg = document.getElementById("signin-error")
} 

onSubmitData = async function (e) {
    e.preventDefault()
    
    let data = new FormData(loginForm)
    let response = await fetch('/login', {method: 'POST', body: data})

    if (response.status === 401) {
        response_data = await response.json()
        if (response_data.detail) {
            errorMsg.className = "error-mes"
            errorMsg.innerText = response_data.detail
            result = false
        }
    } else {
        window.location.href = "/"
    }
    
}