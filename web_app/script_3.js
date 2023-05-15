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
        let now = new Date().getTime()
        timerActive = setInterval(() => {
            console.log(f0rm.nextElementSibling.className)
            if (f0rm.nextElementSibling.className === "timer reset") {
                f0rm.nextElementSibling.className = "timer play"
                clearInterval(timerActive)
            } else if (f0rm.nextElementSibling.className === "timer play") {
                const distance = inputValue - now
                now += 1000
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
        f0rm = this.closest(".timer")
        let timerTitle = f0rm.nextElementSibling.querySelector(".timer-name")
        let timerElements = f0rm.nextElementSibling.querySelectorAll("span")
        inputTitle = f0rm.querySelector(".input_name").value
        let inputDate = f0rm.querySelectorAll(".input-date")[1].value
        console.log(inputDate)
        if (inputDate === '') {
            alert(`Please select a date for the Timer\nTimer name : "${inputTitle}"`)
        } else {
            let inputValue = new Date(inputDate).getTime()
            timerTitle.textContent = `${inputTitle}`
            isPaused = false
            updateDom(f0rm, timerElements, inputValue)
        }

    }

    function reset(e) {
        f1rm = this.closest(".timer")
        f1rm.querySelector("img").setAttribute("src", "./img/svg/pause.svg")
        f1rm.previousElementSibling.hidden = false
        f1rm.hidden = true

        f1rm.className = "timer reset"


    }

    function end(e) {
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

const template = document.querySelector("#newTimer");

function createTime() {
    const clone = template.content.cloneNode(true);
    adder.parentNode.insertBefore(clone, adder)
    timeMe()
}

madder = document.querySelector(".header__add")
adder = document.querySelector("#add-bottom")
adder.addEventListener('click', createTime)
madder.addEventListener('click', createTime)


