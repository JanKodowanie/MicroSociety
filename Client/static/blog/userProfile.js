
window.addEventListener("load", initialize, true); 

function initialize() {
    let edit_button = document.getElementById("edit-account")
    let delete_button = document.getElementById("delete-account")
    let delete_own_button = document.getElementById("delete-own-account")
    let logout_all_button = document.getElementById("logout-all")
    let ban_button = document.getElementById("ban-account")
    let unban_button = document.getElementById("unban-account")

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
    if (ban_button != null) {
        ban_button.addEventListener('click', onBanAccountButtonClicked)
    }
    if (unban_button != null) {
        unban_button.addEventListener('click', onUnbanAccountButtonClicked)
    }
} 

onEditAccountButtonClicked = async function (e) {
    e.preventDefault()
    window.location.href = "/account/edit-form"
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
        window.location.href = "/profiles"
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

onBanAccountButtonClicked = async function (e) {
    e.preventDefault()
    let form = e.target.parentNode
    let url = form.action.concat("", "/ban")
    let response = await fetch(url, {method: 'PATCH'})

    if (response.status !== 204) {
        response_data = await response.json()
        if (response_data.detail) {
            alert(response_data.detail)
        }
    } else {
        window.location.reload()
    }
}

onUnbanAccountButtonClicked = async function (e) {
    e.preventDefault()
    let form = e.target.parentNode
    let url = form.action.concat("", "/unban")
    let response = await fetch(url, {method: 'PATCH'})

    if (response.status !== 204) {
        response_data = await response.json()
        if (response_data.detail) {
            alert(response_data.detail)
        }
    } else {
        window.location.reload()
    }
}