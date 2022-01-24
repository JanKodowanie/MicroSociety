
window.addEventListener("load", initialize, true); 

function initialize() {
    document.getElementById("fullname").addEventListener("change", searchEmployees)
} 

searchEmployees = async function (e) {
    let input = document.getElementById("fullname")

    if (input.value == "") {
        window.location.href = "/admin/employees"
                    
    } else {
        window.location.href = "/admin/employees?fullname=".concat("", input.value)
    }
}