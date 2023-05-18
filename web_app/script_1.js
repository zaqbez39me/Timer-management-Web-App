
let lBtn = document.getElementById("lBtn")
let rBtn = document.getElementById("rBtn")
let title = document.getElementById("title")

let userName = document.querySelector('#name')
let pass = document.querySelector('#pass')
let secPass = document.querySelector('#secPass')

let error1 = document.querySelector('#error1')
let error2 = document.querySelector('#error2')

let cPass = document.getElementById("cPass")

lBtn.onclick = async () => {
    error1.style.maxHeight = "0px"
    error1.style.border = "0px solid #ff0000"
    error2.style.maxHeight = "0px"
    error2.style.border = "0px solid #ff0000"
    if (cPass.style.maxHeight === "0px") {
        if (userName.value !== "" && pass.value !== "") {
            console.log(`{Username : ${userName.value}, Password : ${pass.value} }`)
            lBtn.setAttribute('type', 'submit')
            await login(userName.value, pass.value)
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
rBtn.onclick = async () => {
    console.log("Register button clicked")
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
            await register(userName.value, pass.value)
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

const BACK_IP = "0.0.0.0"
const BACK_PORT = 8080
const baseUrl = `http://${BACK_IP}:${BACK_PORT}`

// register
async function register(username, password) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await fetch(`${baseUrl}/auth/register`, {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: formData,
    });
    console.log(`Sent register request. Response status: ${response.ok}`)
    if (response.ok == true) {
        const answer = await response.json();
        console.log(answer);
        // Register doesn't provide access token
        window.location.assign('/1.html')
    } else{
        // TODO: error handling
    }
}

// login
async function login(username, password) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await fetch(`${baseUrl}/auth/login`, {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: formData,
    });
    console.log(`Sent login request. Response status: ${response.ok}`)
    if (response.ok == true) {
        const answer = await response.json();
        console.log(answer);
        localStorage.setItem('access_token', answer['access_token']);
        localStorage.setItem('refresh_token', answer['refresh_token']);
        localStorage.setItem('token_type', answer['token_type']);
        window.location.assign('/3.html')
    } else{
        // TODO: error handling
    }
}

