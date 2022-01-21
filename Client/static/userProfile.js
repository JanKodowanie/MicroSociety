
window.addEventListener("load", initialize, true); 

function initialize() {
    let edit_buttons = document.getElementsByClassName("edit-account-button");
    let delete_buttons = document.getElementsByClassName("delete-account-button");
    
    for (let i = 0; i < edit_buttons.length; i++) {
        edit_buttons[i].addEventListener('click', onEditAccountButtonClicked);
    }
    for (let i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].addEventListener('click', onDeleteAccountButtonClicked);
    }
} 

onEditAccountButtonClicked = async function (e) {
    e.preventDefault()
}

onDeleteAccountButtonClicked = async function (e) {
    e.preventDefault()
    let form = e.target.parentNode
    let url = form.action
    let response = await fetch(url, {method: 'DELETE'})

    if (response.status !== 200) {
        response_data = await response.json()
        if (response_data.detail) {
            alert(response_data.detail)
        }
    } else {
        window.location.href = "/"
    }
}