const BACK_IP = "0.0.0.0"
const BACK_PORT = 8080
const baseUrl = `http://${BACK_IP}:${BACK_PORT}`

async function login_check() {
    // Checking for necessary info in local storage
    for (let attribute in ['access_token', 'refresh_token', 'token_type']){
        if (!localStorage.getItem(attribute)) {
            return false;
        }
    }

    // Checking for token to be a valid key
    const response = await get_access_token_info(localStorage['access_token'], localStorage['token_type']);
    console.log(response.status);
    return response.status == 200
}

async function get_access_token_info(token, token_type) {
    let formData = new FormData();
    const response = await fetch(`${baseUrl}/token/access/info`, {
        method: "GET",
        headers: {"Authorization": `${token_type} ${token}`},
    });
    return response;
}

async function redirect_if_not_logged() {
    // console.log(localStorage);
    console.log(await get_access_token_info(localStorage['access_token'], localStorage['token_type']));
    if (!(await login_check())) {
        // On fixing CORS uncomment the line after this line
        // window.location.assign('/1.html')
    }
}
// Add this file as script for every html file that has to be checked for login
document.addEventListener('DOMContentLoaded', redirect_if_not_logged(), false);
