var resetForm = null


window.addEventListener("load", initialize, true); 

function initialize() {
    resetForm = document.getElementById("pass-reset-form")
    resetForm.addEventListener("submit", onSubmitData)
} 

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


onSubmitData = async function (e) {
    e.preventDefault()
    let msg = document.getElementById("pass-message")

    let data = new FormData(resetForm)
    let response = await fetch('/password-reset-code', {method: 'POST', body: data})

    if (response.status === 201) {
        data = await response.json()
        msg.className = "error-mes"
        msg.innerText = data.detail
        msg.style.color = "#008000"
        await sleep(1200)
        window.location.href = "/login"
    }
}