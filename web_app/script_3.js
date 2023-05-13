function timeMe() {
    containers = document.getElementsByClassName("timer-container")
    forms = containers[containers.length - 1].getElementsByClassName("timer")
    datePicker = forms[0].querySelectorAll(".input-date")[1]
    const today = new Date().toISOString().split("T")[0]
    datePicker.setAttribute("min", today)


    let timerActive;


    sec = 1000
    minute = sec * 60
    hour = minute * 60
    day = hour * 24

    function updateDom(f0rm, timerElements, inputValue) {
        timerActive = setInterval(() => {
            console.log(f0rm.nextElementSibling.className)
            if (f0rm.nextElementSibling.className === "timer reset") {
                f0rm.nextElementSibling.className = "timer play"
                clearInterval(timerActive)
            } else if (f0rm.nextElementSibling.className === "timer play") {
                const now = new Date().getTime()
                const distance = inputValue - now
                // resetTimer +=now
                console.log(distance)
                const days = Math.floor(distance / day)
                const hours = Math.floor((distance % day) / hour)
                const minutes = Math.floor((distance % hour) / minute)
                const seconds = Math.floor((distance % minute) / sec)
                console.log(days, hours, minutes, seconds)
                if (distance < 0) {
                    end()
                }
                timerElements[0].textContent = `${days}`
                timerElements[1].textContent = `${hours}`
                timerElements[2].textContent = `${minutes}`
                timerElements[3].textContent = `${seconds}`
                f0rm.hidden = true
                f0rm.nextElementSibling.hidden = false
            }
        }, sec)
    }

    function updateCountdown(e) {
        e.preventDefault()
        let timerTitle = this.nextElementSibling.querySelector(".timer-name")
        let timerElements = this.nextElementSibling.querySelectorAll("span")
        let inputTitle = e.target[0].value
        let inputDate = e.target[1].value
        if (inputDate === '') {
            alert(`Please select a date for the Timer\nTimer name : "${inputTitle}"`)
        } else {
            let inputValue = new Date(inputDate).getTime()
            timerTitle.textContent = `${inputTitle}`
            isPaused = false
            updateDom(this, timerElements, inputValue)
        }

    }

    function reset(e) {
        f1rm = this.closest(".timer")
        f1rm.querySelector("img").setAttribute("src", "./img/svg/pause.svg")
        e.preventDefault()
        f1rm.previousElementSibling.hidden = false
        f1rm.hidden = true

        f1rm.className = "timer reset"


    }

    function end(e) {
        e.preventDefault()
        f1rm = this.closest(".timer")
        f1rm.previousElementSibling.hidden = true
        f1rm.hidden = true
        f1rm.nextElementSibling.hidden = false
        f1rm.className = "timer reset"


    }

    function pause() {
        f1rm = this.closest(".timer")
        console.log(f1rm)
        if (f1rm.classList[1] === "play") {
            f1rm.classList.remove("play")
            f1rm.querySelector("img").setAttribute("src", "./img/svg/play.svg")
        } else {
            f1rm.classList.add("play")
            f1rm.querySelector("img").setAttribute("src", "./img/svg/pause.svg")
        }
    }

    function die(){
        this.closest(".timer-container").remove()
    }
    forms[0].addEventListener("submit", updateCountdown)
    forms[0].querySelectorAll(".timer-button")[1].addEventListener("click", die)
    forms[1].querySelectorAll(".timer-button")[1].addEventListener('click', reset)
    forms[1].querySelectorAll(".timer-button")[2].addEventListener('click', end)
    forms[1].querySelector(".timer-button").addEventListener('click', pause)
    forms[2].querySelector(".timer-button").addEventListener('click', die)

}

const template = document.querySelector("#newTimer");

function createTime() {
    const clone = template.content.cloneNode(true);
    adder.parentNode.insertBefore(clone, adder)
    timeMe()
}

adder = document.querySelector("#add-bottom")
adder.addEventListener('click', createTime)

