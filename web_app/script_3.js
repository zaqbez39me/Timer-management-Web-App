
sec = 1000
minute = sec * 60
hour = minute * 60
day = hour * 24


async function getServerTime() {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/time_sync/`, {
        method: "GET",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
    })
    if (!response.ok) {
        window.location.assign('/1.html')
    }
    responseJson = response.json()
    console.log(responseJson["server_time"])
    return new Date(responseJson["server_time"])
}

async function fetchAllTimers() {
    token = sessionStorage.getItem('access_token')
    const response = await fetch(`${baseUrl}/timers/`, {
        method: "GET",
        credentials: "include",
        headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
    })
    if (!response.ok) {
        window.location.assign('/1.html')
    }
    responseJson = response.json()
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
    actualTime = Date.now()
    timeError = actualTime - clientTime
    // Date.setTime(clientTime)
    for (let i = 0; i < timers.length; ++i) {
        timers["time_left"] = Math.floor((Date.now() + timeError) / 1000) - timers["time_left"]
    }
    console.log("timers")
    console.log(timers)
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
    if (!response.ok) {
        window.location.assign('/1.html')
    }
    responseJson = response.json()
    console.log(responseJson);
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
    if (!response.ok) {
        window.location.assign('/1.html')
    }
    responseJson = response.json()
    console.log(responseJson);

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
    if (!response.ok) {
        window.location.assign('/1.html')
    }
    responseJson = response.json()
    console.log(responseJson);

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
    if (!response.ok) {
        window.location.assign('/1.html')
    }
    responseJson = response.json()
    console.log(responseJson);

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
    if (!response.ok) {
        window.location.assign('/1.html')
    }
    if (response.ok) {
        responseJson = response.json()
        console.log(responseJson);
    }
}

async function timeMe() { // Функция добавляет таймеру слушателей событий для кнопок


    containers = document.getElementsByClassName("timer-container")
    forms = containers[containers.length - 1].getElementsByClassName("timer")
    datePicker = forms[0].querySelectorAll(".input-date")[1]
    const today = new Date().toISOString().split("T")[0]
    datePicker.setAttribute("min", today)

    // Интервал
    let timerActive;

    async function updateDom(f0rm, timerElements, inputValue, timerTitle) {
        let now = new Date().getTime()
        let nowTime = 0
        console.log(Math.floor((inputValue - now) / sec), timerTitle)
        await removeTimer(timerTitle)
        await addTimer(timerTitle, Math.floor((inputValue) / sec))
        await resumeTimer(timerTitle)
        timerActive = setInterval(async () => {
            if (f0rm.nextElementSibling.className === "timer reset") {
                f0rm.nextElementSibling.className = "timer play"

                clearInterval(timerActive)
            } else if (f0rm.nextElementSibling.className === "timer play") {
                f0rm.hidden = true
                f0rm.nextElementSibling.hidden = false
                const distance = inputValue - nowTime
                nowTime += sec
                const days = Math.floor(distance / day)
                const hours = Math.floor((distance % day) / hour)
                const minutes = Math.floor((distance % hour) / minute)
                const seconds = Math.floor((distance % minute) / sec)
                // console.log(days, hours, minutes, seconds)
                if (distance < 0) {
                    f1rm = f0rm.nextElementSibling
                    await resetTimer(f1rm.querySelector(".timer-name").textContent)
                    f1rm.previousElementSibling.hidden = true
                    f1rm.hidden = true
                    f1rm.nextElementSibling.hidden = false
                    f1rm.className = "timer reset"
                }
                timerElements[0].textContent = `${days}`
                timerElements[1].textContent = `${hours}`
                timerElements[2].textContent = `${minutes}`
                timerElements[3].textContent = `${seconds}`
            }
        }, sec)
    }

    function updateCountdown(e) {
        f0rm = this.closest(".timer")
        let timerTitle = f0rm.nextElementSibling.querySelector(".timer-name")
        let finishTimerTitle = f0rm.nextElementSibling.nextElementSibling.querySelector(".timer-name")
        let timerElements = f0rm.nextElementSibling.querySelectorAll("span")
        inputTitle = f0rm.querySelector(".input_name").value
        let inputDate = f0rm.querySelectorAll(".input-date")[1].value
        if (inputDate === '') {
            alert(`Please select a date for the Timer\nTimer name : "${inputTitle}"`)
        } else {
            var a = inputDate.split(':'); // split it at the colons
            var inputValue = (+a[0]) * 60 * 60 + (+a[1]) * 60 + (+a[2]);
            timerTitle.textContent = `${inputTitle}`
            finishTimerTitle.textContent = `${inputTitle}`
            isPaused = false
            updateDom(f0rm, timerElements, inputValue * 1000, inputTitle)
        }

    }

    async function reset(e) {
        f1rm = this.closest(".timer")
        await resetTimer(f1rm.querySelector(".timer-name").textContent)
        f1rm.querySelector("img").setAttribute("src", "./img/svg/pause.svg")
        f1rm.previousElementSibling.hidden = false
        f1rm.hidden = true

        f1rm.className = "timer reset"


    }

    async function end(e) {
        await removeTimer(f1rm.querySelector(".timer-name").textContent)
        f1rm = this.closest(".timer")
        f1rm.previousElementSibling.hidden = true
        f1rm.hidden = true
        f1rm.nextElementSibling.hidden = false
        f1rm.className = "timer reset"

    }

    async function pause() {
        f1rm = this.closest(".timer")
        if (f1rm.classList[1] === "play") {
            await stopTimer(f1rm.querySelector(".timer-name").textContent)
            f1rm.classList.remove("play")
            f1rm.querySelector("img").setAttribute("src", "./img/svg/play.svg")
        } else {
            await resumeTimer(f1rm.querySelector(".timer-name").textContent)
            f1rm.classList.add("play")
            f1rm.querySelector("img").setAttribute("src", "./img/svg/pause.svg")
        }
    }

    function die() {
        this.closest(".timer-container").remove()
    }

    forms[0].querySelector(".timer-button").addEventListener("click", updateCountdown)
    forms[0].querySelectorAll(".timer-button")[1].addEventListener("click", die)

    forms[1].querySelector(".timer-button").addEventListener('click', pause)
    forms[1].querySelectorAll(".timer-button")[1].addEventListener('click', reset)
    forms[1].querySelectorAll(".timer-button")[2].addEventListener('click', end)

    forms[2].querySelector(".timer-button").addEventListener('click', die)

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

// document.addEventListener('DOMContentLoaded', getAllTimers(), false);
