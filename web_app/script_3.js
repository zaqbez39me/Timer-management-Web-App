sec = 1000
minute = sec * 60
hour = minute * 60
day = hour * 24

refreshTime = true
function refresh(timers){
    for (let i=0; i<timers.length; i++){
        obj = timers[i]
        console.log(obj)
        document.querySelector(".header__add").click()
        containers = document.getElementsByClassName("timer-container")
        forms = containers[containers.length - 1].getElementsByClassName("timer")
        forms[0].querySelector(".input_name").value = obj["name"]
        let hours = Math.floor(obj["time_left"]/3600)
        let minutes = Math.floor((obj["time_left"] - (hours * 3600)) / 60);
        let seconds = obj["time_left"] - (hours * 3600) - (minutes * 60);
        if (hours   < 10) {hours   = "0"+hours;}
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        forms[0].querySelectorAll(".input-date")[1].value= hours+':'+minutes+':'+seconds;
        forms[0].querySelector(".timer-button").click()
        if (!obj["active"]){
            console.log(forms[1].querySelector(".timer-button"))
            forms[1].querySelector(".timer-button").click()
        }
        console.dir(timers)

    }
    refreshTime = false
}


async function getServerTime() {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/time_sync/`, {
        method: "GET",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
    })
    // if (!response.ok) {
    //     window.location.assign('/login')
    // }
    responseJson = await response.json()
    console.log(responseJson["server_time"])
    return Math.floor((new Date(responseJson["server_time"])).getTime() / 1000)
}

async function fetchAllTimers() {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/timers/`, {
        method: "GET",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
    })
    // if (!response.ok) {
    //     window.location.assign('/login')
    // }
    responseJson = await response.json()
    console.log(responseJson)
    return responseJson
}

function ChristianAlgorithm(serverTime, requestTime, responseTime) {
    processDelayLatency = responseTime - requestTime
    clientTime = serverTime + Math.floor(processDelayLatency / 2)
    return clientTime
}

// Use this function
// Returns list of jsons and syncronizes time with servers
// {
//     "name": "New12 Timer",
//     "start_time": "2023-05-19 20:07:32.388752",
//     "duration_seconds": 13947,
//     "time_left": 13947,
//     "active": false
// },
async function getAllTimers() {
    requestTime = Math.floor(Date.now() / 1000)
    serverTime = await getServerTime()
    responseTime = Math.floor(Date.now() / 1000)
    timers = await fetchAllTimers()
    clientTime = ChristianAlgorithm(serverTime, requestTime, responseTime)
    actualTime = Math.floor(Date.now() / 1000)
    timeError = actualTime - clientTime
    // Date.setTime(clientTime)
    for (let i = 0; i < timers.length; ++i) {
        // console.log(`Time left: ${timers[i]["time_left"]}`)
        if (timers[i]["active"]) {
            end_time = Math.floor((new Date(timers[i]["start_time"])).getTime() / 1000) + timers[i]["duration_seconds"]
            current_time = Math.floor(new Date() / 1000) + new Date().getTimezoneOffset() * 60
            // console.log('start time in seconds: ', Math.floor((new Date(timers[i]["start_time"])).getTime() / 1000))
            // console.log('duration seconds ', timers[i]["duration_seconds"])
            // console.log('end time ', end_time)
            // console.log('current time ', current_time)
            // console.log('time error ', timeError)
            timers[i]["time_left"] = end_time - current_time + timeError
            if (timers[i]["time_left"] <= 0) {
                timers[i]["time_left"] = 0
                timers[i]["active"] = false
            }
            // timers[i]["time_left"] = Math.floor(((Date.now()) + timeError * 1000) / 1000) - Math.floor((new Date(timers[i]["start_time"])).getTime() / 1000)
            // console.log(`Time left: ${timers[i]["time_left"]}`)
        }
    }
    // console.log("timers")
    // console.log(timers)
    refresh(timers)
    return timers
}

// add Timer
async function addTimer(timerName, durationInSeconds) {
    token = sessionStorage.getItem('access_token')
    console.log(token)
    body = JSON.stringify({
        "name": timerName,
        "duration_seconds": durationInSeconds
    })
    console.log(body)
    const response = await fetch(`${baseUrl}/timers/add`, {
        method: "POST",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: body
    })
    if (!response.ok){
        if(response.status === 401) {
            window.location.assign('/login')
        } else if(response.status === 409){
            alert(`Please select a unique timer name!"`)
            return false;
        }
    }
    return true;
    // if (!response.ok) {
    //
    // }
    // responseJson = response.json()
    // console.log(responseJson);
}

async function stopTimer(timerName) {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/timers/stop`, {
        method: "POST",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({
            "name": timerName
        })
    })
    // if (!response.ok) {
    //     window.location.assign('/login')
    // }
    // responseJson = response.json()
    // console.log(responseJson);

}
async function resumeTimer(timerName) {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/timers/resume`, {
        method: "POST",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({
            "name": timerName
        })
    })
    // if (!response.ok) {
    //     window.location.assign('/login')
    // }
    // responseJson = response.json()
    // console.log(responseJson);

}
async function resetTimer(timerName, durationInSeconds) {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/timers/reset`, {
        method: "POST",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({
            "name": timerName
        })
    })
    // if (!response.ok) {
    //     window.location.assign('/login')
    // }
    // responseJson = response.json()
    // console.log(responseJson);

}
async function removeTimer(timerName) {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/timers/remove`, {
        method: "DELETE",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({
            "name": timerName
        })
    })
    // if (!response.ok) {
    //     window.location.assign('/login')
    // }
    if (response.ok) {
        responseJson = await response.json()
        console.log(responseJson);
    }
}

async function timeMe() { // Функция добавляет таймеру слушателей событий для кнопок

    containers = document.getElementsByClassName("timer-container")
    forms = containers[containers.length - 1].getElementsByClassName("timer")


    // Интервал
    let timerActive;

    async function updateDom(f0rm, timerElements, inputValue, timerTitle) {
        let now = new Date().getTime()
        let nowTime = 0
        console.log(Math.floor((inputValue) / sec), timerTitle)
        if(!(await addTimer(timerTitle, Math.floor((inputValue) / sec))))
            if (!refreshTime)
                return;
        await resumeTimer(timerTitle)
        f0rm.hidden = true
        f0rm.nextElementSibling.hidden = false
        let distance = inputValue - nowTime
        const days = Math.floor(distance / day)
        const hours = Math.floor((distance % day) / hour)
        const minutes = Math.floor((distance % hour) / minute)
        const seconds = Math.floor((distance % minute) / sec)
        nowTime += sec
        timerElements[0].textContent = `${days}`
        timerElements[1].textContent = `${hours}`
        timerElements[2].textContent = `${minutes}`
        timerElements[3].textContent = `${seconds}`
        f0rm.nextElementSibling.className = "timer play"
        const id = timerElements[0].closest(".dig-time")
        if (distance===0){
            id.style.background = "linear-gradient(62.99deg, #25EFAC 18.31%, #21BE57 83.56%)"
            id.style.webkitBackgroundClip= "text"
        }else {
            id.style.background = "linear-gradient(62.99deg, #EEF1F0 7.18%, #71757E 83.56%)"
            id.style.webkitBackgroundClip = "text"
        }
        f0rm.nextElementSibling.querySelectorAll(".timer-button")[0].disabled = false
        f0rm.nextElementSibling.querySelectorAll(".timer-button")[1].disabled = false
        timerActive = setInterval(async () => {
            if (f0rm.nextElementSibling.className === "timer reset"){
                id.style.background = "linear-gradient(62.99deg, #EEF1F0 7.18%, #71757E 83.56%)"
                id.style.webkitBackgroundClip = "text"
                nowTime = 0
                f0rm.nextElementSibling.className = "timer"
                distance = inputValue - nowTime
                nowTime += sec
                const days = Math.floor(distance / day)
                const hours = Math.floor((distance % day) / hour)
                const minutes = Math.floor((distance % hour) / minute)
                const seconds = Math.floor((distance % minute) / sec)
                // console.log(days, hours, minutes, seconds)

                timerElements[0].textContent = `${days}`
                timerElements[1].textContent = `${hours}`
                timerElements[2].textContent = `${minutes}`
                timerElements[3].textContent = `${seconds}`
                f0rm.nextElementSibling.querySelector(".timer-button").disabled = false
            }
            else if (f0rm.nextElementSibling.className === "timer settings") {

                // f0rm.nextElementSibling.className = "timer play"
                clearInterval(timerActive)
                f0rm.querySelector(".timer-button").disabled = false
            } else if (f0rm.nextElementSibling.className === "timer play") {
                f0rm.hidden = true
                f0rm.nextElementSibling.hidden = false
                let distance = inputValue - nowTime
                nowTime += sec
                if (distance < 0) {
                    id.style.background = "linear-gradient(62.99deg, #25EFAC 18.31%, #21BE57 83.56%)"
                    id.style.webkitBackgroundClip= "text"
                    f1rm = f0rm.nextElementSibling
                    f1rm.className = "timer settings"
                    f0rm.nextElementSibling.querySelectorAll(".timer-button")[0].disabled = true
                    // f0rm.nextElementSibling.querySelectorAll(".timer-button")[2].click()
                } else {
                    const days = Math.floor(distance / day)
                    const hours = Math.floor((distance % day) / hour)
                    const minutes = Math.floor((distance % hour) / minute)
                    const seconds = Math.floor((distance % minute) / sec)
                    // console.log(days, hours, minutes, seconds)

                    timerElements[0].textContent = `${days}`
                    timerElements[1].textContent = `${hours}`
                    timerElements[2].textContent = `${minutes}`
                    timerElements[3].textContent = `${seconds}`
                    if (distance===0){
                        id.style.background = "linear-gradient(62.99deg, #25EFAC 18.31%, #21BE57 83.56%)"
                        id.style.webkitBackgroundClip= "text"
                    }
                }
            }
        }, sec)
    }

    function updateCountdown(e) {
        f0rm = this.closest(".timer")
        let timerTitle = f0rm.nextElementSibling.querySelector(".timer-name")
        let timerElements = f0rm.nextElementSibling.querySelectorAll("span")
        inputTitle = f0rm.querySelector(".input_name").value
        let inputDate = f0rm.querySelectorAll(".input-date")[1].value
        let a = inputDate.split(':'); // split it at the colons
        let inputValue = (+a[0]) * 60 * 60 + (+a[1]) * 60 + (+a[2]);
        timerTitle.textContent = `${inputTitle}`
        isPaused = false
        updateDom(f0rm, timerElements, inputValue * 1000, inputTitle)
    }

    async function settings(e) {
        f1rm = this.closest(".timer")
        if (f1rm.className === "timer play" || f1rm.className === "timer") {
            f1rm.previousElementSibling.querySelector(".timer-button").disabled = true
        }
        await removeTimer(f1rm.querySelector(".timer-name").textContent)
        f1rm.querySelector("img").setAttribute("src", "./img/svg/pause.svg")
        f1rm.previousElementSibling.hidden = false
        f1rm.hidden = true
        if (f1rm.className !== "timer settings") {
            f1rm.className = "timer settings"
            f1rm.querySelectorAll(".timer-button")[1].disabled = true
        }



    }

    async function end(e) {
        f1rm = this.closest(".timer")
        await removeTimer(f1rm.querySelector(".timer-name").textContent)
        f1rm.className = "timer settings"
        this.closest(".timer-container").remove()

    }
    async function reset() {
        f1rm = this.closest(".timer")
        f1rm.querySelector(".timer-button").disabled = true
        await resetTimer(f1rm.querySelector(".timer-name").textContent)
        f1rm.className = "timer reset"
        f1rm.querySelector("img").setAttribute("src", "./img/svg/play.svg")
    }

    async function pause() {
        f1rm = this.closest(".timer")
        if (f1rm.classList[1] === "play") {
            await stopTimer(f1rm.querySelector(".timer-name").textContent)
            f1rm.classList.remove("play")
            f1rm.querySelector("img").setAttribute("src", "./img/svg/play.svg")
        } else if (f1rm.classList[1] !== "settings"){
            await resumeTimer(f1rm.querySelector(".timer-name").textContent)
            f1rm.classList.add("play")
            f1rm.querySelector("img").setAttribute("src", "./img/svg/pause.svg")
        }
    }

    function die(){
        this.closest(".timer-container").remove()
    }

    forms[0].querySelector(".timer-button").addEventListener("click", updateCountdown)
    forms[0].querySelectorAll(".timer-button")[1].addEventListener("click", die)

    forms[1].querySelector(".timer-button").addEventListener('click', pause)
    forms[1].querySelectorAll(".timer-button")[1].addEventListener('click', reset)
    forms[1].querySelectorAll(".timer-button")[2].addEventListener('click', settings)
    forms[1].querySelectorAll(".timer-button")[3].addEventListener('click', end)


}


function createTime() {
    const clone = template.content.cloneNode(true);
    adder.parentNode.insertBefore(clone, adder)
    // Новый таймер был создан
    timeMe()
}

// Шаблон таймера
const template = document.querySelector("#newTimer");

// Кнопки добавления таймеров
madder = document.querySelector(".header__add")
adder = document.querySelector("#add-bottom")
adder.addEventListener('click', createTime)
madder.addEventListener('click', createTime)

let exitBtn = document.querySelector(".header__exit")
document.addEventListener('DOMContentLoaded', getAllTimers(), false);
