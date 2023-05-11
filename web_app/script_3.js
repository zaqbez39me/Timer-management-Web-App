forms = document.getElementsByClassName("timer")
datePicker = document.forms[0].querySelector(".input-date")
inputTitle = ''
inputDate = ''
inputValue = Date
let timerActive;
isPaused = false
const today = new Date().toISOString().split("T")[0]
datePicker.setAttribute("min", today)

timerTitle = forms[1].querySelector(".timer-name")
timerElements = forms[1].querySelectorAll("span")
firstDistance = 0
sec = 1000
minute = sec * 60
hour = minute * 60
day = hour * 24

function updateDom() {
    timerActive = setInterval(() => {
        if (!isPaused) {
            const now = new Date().getTime()
            const distance = inputValue - now
            // resetTimer +=now
            console.log(distance)
            const days = Math.floor(distance / day)
            const hours = Math.floor((distance % day) / hour)
            const minutes = Math.floor((distance % hour) / minute)
            const seconds = Math.floor((distance % minute) / sec)
            console.log(days, hours, minutes, seconds)
            if (days === 0 && hours === 0 && minutes === 0 && seconds === 0){
                end()
            }
            timerElements[0].textContent = `${days}`
            timerElements[1].textContent = `${hours}`
            timerElements[2].textContent = `${minutes}`
            timerElements[3].textContent = `${seconds}`
            forms[0].hidden = true
            forms[1].hidden = false
        }
    }, sec)
}

function updateCountdown(e) {
    e.preventDefault()
    inputTitle = e.srcElement[0].value
    inputDate = e.srcElement[1].value
    console.log(inputTitle, inputDate)
    if (inputDate === '') {
        alert(`Please select a date for the Timer\nTimer name : "${inputTitle}"`)
    } else {
        inputValue = new Date(inputDate).getTime()
        timerTitle.textContent = `${inputTitle}`
        updateDom()
    }

}

function reset(e) {
    e.preventDefault()
    forms[0].hidden = false
    forms[1].hidden = true

    clearInterval(timerActive)

    inputTitle = ""
    inputDate = ""

}

function end(e) {
    e.preventDefault()
    forms[0].hidden = true
    forms[1].hidden = true
    forms[2].hidden = false
    clearInterval(timerActive)
    inputTitle = ""
    inputDate = ""


}

forms[0].addEventListener("submit", updateCountdown)
forms[1].querySelectorAll(".timer-button")[1].addEventListener('click', reset)
forms[1].querySelectorAll(".timer-button")[2].addEventListener('click', end)
forms[1].querySelectorAll(".timer-button")[0].addEventListener('click', () => {
    if (isPaused) {
        isPaused = false
        forms[1].querySelector("img").setAttribute("src", "./img/svg/pause.svg")
    } else {
        isPaused = true
        forms[1].querySelector("img").setAttribute("src", "./img/svg/play.svg")
    }
})
