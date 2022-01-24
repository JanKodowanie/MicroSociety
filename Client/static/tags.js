
window.addEventListener("load", initialize, true); 

function initialize() {
    document.getElementById("tag-name").addEventListener("change", searchTags)
} 

searchTags = async function (e) {
    let input = document.getElementById("tag-name")

    if (input.value == "") {
        window.location.href = "/tags"
                    
    } else {
        window.location.href = "/tags?name_contains=".concat("", input.value)
    }
}