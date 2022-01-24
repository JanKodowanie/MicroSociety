
window.addEventListener("load", initialize, true); 

function initialize() {
    let edit_button = document.getElementById("edit-account")
    let delete_button = document.getElementById("delete-account")
    let delete_own_button = document.getElementById("delete-own-account")
    let logout_all_button = document.getElementById("logout-all")

    if (edit_button != null) {
        edit_button.addEventListener('click', onEditAccountButtonClicked)
    }
    if (delete_button != null) {
        delete_button.addEventListener('click', onDeleteAccountButtonClicked)
    }
    if (delete_own_button != null) {
        delete_own_button.addEventListener('click', onDeleteOwnAccountButtonClicked)
    }
    if (logout_all_button != null) {
        logout_all_button.addEventListener('click', onLogoutAllButtonClicked)
    }
} 

onEditAccountButtonClicked = async function (e) {
    e.preventDefault()
}

onLogoutAllButtonClicked = async function (e) {
    e.preventDefault()
    await fetch("/logout-all", {method: 'POST'})
    window.location.href = "/login"
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
        window.location.href = "/admin/employees"
    }
}

onDeleteOwnAccountButtonClicked = async function (e) {
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