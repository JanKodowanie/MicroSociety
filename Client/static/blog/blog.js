var post_form = null
window.addEventListener("load", initialize, true); 

function initialize() {
    let edit_buttons = document.getElementsByClassName("edit-post-button");
    let delete_buttons = document.getElementsByClassName("delete-post-button");
    let like_buttons = document.getElementsByClassName("create-post-like");
    let unlike_buttons = document.getElementsByClassName("delete-post-like");
    let discussion_buttons = document.getElementsByClassName("show-discussion");
    post_form = document.getElementById("new-post-form")
    if (post_form != null) {
        post_form.addEventListener("submit", onSubmitPostData);
    }
        
    for (let i = 0; i < edit_buttons.length; i++) {
        edit_buttons[i].addEventListener('click', onEditPostButtonClicked);
    }
    for (let i = 0; i < delete_buttons.length; i++) {
        delete_buttons[i].addEventListener('click', onDeletePostButtonClicked);
    }
    for (let i = 0; i < like_buttons.length; i++) {
        like_buttons[i].addEventListener('click', onLikePostButtonClicked);
    }
    for (let i = 0; i < unlike_buttons.length; i++) {
        unlike_buttons[i].addEventListener('click', onUnlikePostButtonClicked);
    }
    for (let i = 0; i < discussion_buttons.length; i++) {
        discussion_buttons[i].addEventListener('click', onDiscussionButtonClicked);
    }
} 

onEditPostButtonClicked = async function (e) {
    e.preventDefault()
}

onDeletePostButtonClicked = async function (e) {
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
    response_data = await response.json()
    if (response.status !== 201) {
        alert(response_data.detail)
    } else {
        let url = "/post/" + response_data.id
        let post_ready = false
        while (!post_ready) {
            let response = await fetch(url, {method: 'GET'})
            if (response.status === 200) {
                post_ready = true
            }
        }
        window.location.href = url
    }
}

onDiscussionButtonClicked = async function (e) {
    e.preventDefault()
    let form = e.target.parentNode
    let url = form.action
    let response = await fetch(url, {method: 'GET'})

    if (response.status !== 200) {
        response_data = await response.json()
        if (response_data.detail) {
            alert(response_data.detail)
        }
    } else {
        window.location.href = url
    }
}

onLikePostButtonClicked = async function (e) {
    e.preventDefault()
    let form = e.target.parentNode
    let url = form.action
    let response = await fetch(url, {method: 'POST'})

    if (response.status !== 204) {
        response_data = await response.json()
        if (response_data.detail) {
            alert(response_data.detail)
        }
    } else {
        e.target.removeEventListener('click', onLikePostButtonClicked)
        e.target.addEventListener('click', onUnlikePostButtonClicked)
        e.target.className = "button1 delete-post-like"
        e.target.innerHTML = "–"
        let like_count = form.parentNode.getElementsByClassName("like-count")[0]
        let current_likes = parseInt(like_count.innerHTML.replace('+', ''), 10) + 1
        like_count.innerHTML = '+'.concat('', current_likes)
    }
}

onUnlikePostButtonClicked = async function (e) {
    e.preventDefault()
    let form = e.target.parentNode
    let url = form.action
    let response = await fetch(url, {method: 'DELETE'})

    if (response.status !== 204) {
        response_data = await response.json()
        if (response_data.detail) {
            alert(response_data.detail)
        }
    } else {
        e.target.addEventListener('click', onLikePostButtonClicked)
        e.target.removeEventListener('click', onUnlikePostButtonClicked)
        e.target.className = "button1 create-post-like"
        e.target.innerHTML = "+"
        let like_count = form.parentNode.getElementsByClassName("like-count")[0]
        let current_likes = parseInt(like_count.innerHTML.replace('+', ''), 10) - 1
        like_count.innerHTML = '+'.concat('', current_likes)
    }
}