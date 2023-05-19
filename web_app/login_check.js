const BACK_IP = "0.0.0.0"
const BACK_PORT = 8080
const baseUrl = `http://${BACK_IP}:${BACK_PORT}`

async function login_check() {
    // Checking for necessary info in local storage

    console.log(sessionStorage.getItem('access_token'))
    if (sessionStorage.getItem('access_token') === null) {
        console.log("Local storage is empty")
        return false;
    }
    console.log(sessionStorage.getItem('refresh_token'))
    if (sessionStorage.getItem('refresh_token') === null) {
        console.log("Local storage is empty")
        return false;
    }
    console.log(sessionStorage.getItem('token_type'))
    if (sessionStorage.getItem('token_type') === null) {
        console.log("Local storage is empty")
        return false;
    }

    // Checking for token to be a valid key
    const response = await get_access_token_info(sessionStorage.getItem('access_token'), sessionStorage.getItem('token_type'));
    console.log(`Is valid key: ${response.ok}`);
    return response.ok
}

async function get_access_token_info(token, token_type) {
    let formData = new FormData();
    const response = await fetch(`${baseUrl}/token/access/info`, {
        method: "GET",
        credentials: "include",
        headers: { "Authorization": `Bearer ${token}` },
    });
    return response;
}

async function redirect_if_not_logged() {
    // console.log(sessionStorage);
    console.log(await get_access_token_info(sessionStorage['access_token'], sessionStorage['token_type']));
    if (!(await login_check())) {
        // On fixing CORS uncomment the line after this line

        window.location.assign('/1.html')
    }
}
// Add this file as script for every html file that has to be checked for login
document.addEventListener('DOMContentLoaded', redirect_if_not_logged(), false);
// window.onload = function () { redirect_if_not_logged(); }
