var comment_form = null
window.addEventListener("load", initialize, true); 

function initialize() {
    let post_edit_button = document.getElementsByClassName("edit-post-button");
    let post_delete_button = document.getElementsByClassName("delete-post-button");
    let comment_edit_buttons = document.getElementsByClassName("edit-comment-button");
    let comment_delete_buttons = document.getElementsByClassName("delete-comment-button");
    let like_button = document.getElementsByClassName("create-post-like");
    let unlike_button = document.getElementsByClassName("delete-post-like");


    comment_form = document.getElementById("new-comment-form")
    if (comment_form != null) {
        comment_form.addEventListener("submit", onSubmitCommentData);
    }
    if (post_edit_button.length > 0) {
        post_edit_button[0].addEventListener("click", onEditPostButtonClicked);
    }
    if (post_delete_button.length > 0) {
        post_delete_button[0].addEventListener("click", onDeletePostButtonClicked);
    }
    if (like_button.length > 0) {
        like_button[0].addEventListener("click", onLikePostButtonClicked);
    }
    if (unlike_button.length > 0) {
        unlike_button[0].addEventListener("click", onUnlikePostButtonClicked);
    }
    for (let i = 0; i < comment_edit_buttons.length; i++) {
        comment_edit_buttons[i].addEventListener('click', onEditCommentButtonClicked);
    }
    for (let i = 0; i < comment_delete_buttons.length; i++) {
        comment_delete_buttons[i].addEventListener('click', onDeleteCommentButtonClicked);
    }

} 

onEditPostButtonClicked = async function (e) {
    e.preventDefault()
}

onEditCommentButtonClicked = async function (e) {
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
        window.location.href = '/'
    }
}

onDeleteCommentButtonClicked = async function (e) {
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
        form.parentNode.parentNode.remove()
    }
}

onSubmitCommentData = async function (e) {
    e.preventDefault()
    let data = new FormData(comment_form)
    let url = comment_form.action
    let response = await fetch(url, {method: 'POST', body: data})
    response_data = await response.json()
    if (response.status !== 201) {
        alert(response_data.detail)
    } else {
        window.location.reload()
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