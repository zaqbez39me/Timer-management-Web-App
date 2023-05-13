let lBtn = document.getElementById("lBtn")
let rBtn = document.getElementById("rBtn")
let title = document.getElementById("title")

let userName = document.querySelector('#name')
let pass = document.querySelector('#pass')
let secPass = document.querySelector('#secPass')

let error1 = document.querySelector('#error1')
let error2 = document.querySelector('#error2')

let cPass = document.getElementById("cPass")

lBtn.onclick = () => {
    error1.style.maxHeight = "0px"
    error1.style.border = "0px solid #ff0000"
    error2.style.maxHeight = "0px"
    error2.style.border = "0px solid #ff0000"
    if (cPass.style.maxHeight === "0px") {
        if (userName.value !== "" && pass.value !== "") {
            console.log(`{Username : ${userName.value}, Password : ${pass.value} }`)
            lBtn.setAttribute('type', 'submit')
        } else {
            error2.style.maxHeight = "50px"
            error2.style.border = "1px solid #ff0000"
        }
    } else {
        cPass.style.maxHeight = "0px";
        cPass.style.border = "0"
        title.innerHTML = "Login"
        rBtn.classList.add("disable")
        lBtn.classList.remove("disable")

        // window.location.href = "3.html";
    }
}
rBtn.onclick = () => {
    error1.style.maxHeight = "0px"
    error1.style.border = "0px solid #ff0000"
    error2.style.maxHeight = "0px"
    error2.style.border = "0px solid #ff0000"
    if (cPass.style.maxHeight === "50px") {
        if (pass.value === secPass.value && userName.value !== "") {
            error1.style.maxHeight = "0px"
            error1.style.border = "0px solid #ff0000"
            console.log(`{New Username : ${userName.value}, New Password : ${pass.value}}`)
            rBtn.setAttribute('type','submit')
        } else {
            error1.style.maxHeight = "50px"
            error1.style.border = "1px solid #ff0000"
        }
    } else {
        cPass.style.maxHeight = "50px"
        cPass.style.border = "1px solid #E8E8E8"
        title.innerHTML = "Register"
        rBtn.classList.remove("disable")
        lBtn.classList.add("disable")
    }
}
rBtn.onclick(undefined)
