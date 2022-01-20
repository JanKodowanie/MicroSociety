
window.addEventListener("load", initialize, true); 

function initialize() {
    let logoutLink = document.getElementById("logout")
    if (logoutLink !== null) {
        logoutLink.addEventListener("click", onLogoutClicked)
    }
} 

onLogoutClicked = async function (e) {
    e.preventDefault()
    await fetch('/logout', {method: 'GET'})
    window.location.href = "/"
}