
window.addEventListener("load", initialize, true); 

function initialize() {
    document.getElementById("username").addEventListener("change", searchUsers)
} 

searchUsers = async function (e) {
    let input = document.getElementById("username")

    if (input.value == "") {
        window.location.href = "/profiles"
                    
    } else {
        window.location.href = "/profiles?username=".concat("", input.value)
    }
}