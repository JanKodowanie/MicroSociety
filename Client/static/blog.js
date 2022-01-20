var post_form = null
window.addEventListener("load", initialize, true); 

function initialize() {
    let edit_buttons = document.getElementsByClassName("edit-post-button");
    let delete_buttons = document.getElementsByClassName("delete-post-button");
    post_form = document.getElementById("new-post-form")
    post_form.addEventListener("submit", onSubmitPostData)
    
    for (let i = 0; i < edit_buttons.length; i++) {
        edit_buttons[i].addEventListener('click', onEditButtonClicked);
    }
    for (let i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].addEventListener('click', onDeleteButtonClicked);
    }
} 

onEditButtonClicked = async function (e) {
    e.preventDefault()
    console.log("test")
}

onDeleteButtonClicked = async function (e) {
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
        form.parentNode.parentNode.remove()
    }
}

onSubmitPostData = async function (e) {
    e.preventDefault()
    
    let data = new FormData(post_form)
    let response = await fetch('/post', {method: 'POST', body: data})
    if (response.status !== 201) {
        response_data = await response.json()
        console.log(response_data)
        alert(response_data.detail)
    } else {
        window.location.reload()
    }
}