let lBtn = document.getElementById("lBtn")
let rBtn = document.getElementById("rBtn")
let title = document.getElementById("title")

let userName = document.querySelector('#name')
let pass = document.querySelector('#pass')
let secPass = document.querySelector('#secPass')

let error1 = document.querySelector('#error1')
let error2 = document.querySelector('#error2')
let error3 = document.querySelector('#error3')

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
    error3.style.maxHeight = "0px"
    error3.style.border = "0px solid #ff0000"
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
    try {
    const response = await fetch(`${baseUrl}/auth/register`, {
        method: "POST",
        credentials: "include",
        headers: { "Accept": "application/json" },
        body: formData,
    });
    console.log(`Sent register request. Response status: ${response.ok}`)
    if (response.ok == true) {
        const answer = await response.json();
        console.log(answer);
        // Register doesn't provide access token
        window.location.assign('/1.html')
        return true
    } else{
        // TODO: error handling
        error3.style.maxHeight = "50px"
        error3.style.border = "1px solid #ff0000"
        return false
    }} catch (error) {
        console.log("ERROR Registration")
        console.log(error)
    }
}

// login
async function login(username, password) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await fetch(`${baseUrl}/auth/login`, {
        method: "POST",
        credentials: "include",
        headers: { "Accept": "application/json" },
        body: formData,
    });
    console.log('Cookie');
    console.log(response.headers.getSetCookie())
    console.log(response.headers);
    console.log(response.headers['set-cookie'])
    console.log(response.headers.get('set-cookie')); // undefined 
    console.log(document.cookie); // nope 
    

    console.log(`Sent login request. Response status: ${response.ok}`)
    if (response.ok) {
        console.log('authorized')
        const answer = await response.json();
        console.log(answer);
        sessionStorage.setItem('access_token', answer['access_token']);
        sessionStorage.setItem('refresh_token', answer['refresh_token']);
        sessionStorage.setItem('token_type', answer['token_type']);
        console.log(sessionStorage.getItem('access_token'))
        console.log(sessionStorage.getItem('refresh_token'))
        console.log(sessionStorage.getItem('token_type'))
        // window.location.assign('/3.html')
        return true
    } else{
        // TODO: error handling
        console.log('Unauthorized')
        error2.style.maxHeight = "50px"
        error2.style.border = "1px solid #ff0000"
        return false
    }
}

