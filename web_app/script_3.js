forms = document.getElementsByClassName("timer")
datePicker = document.forms[0].querySelector(".input-date")
inputTitle = ''
inputDate = ''
inputValue = Date
let timerActive;
isPaused = false
shouldReset = false
resetTimer = 0
const today = new Date().toISOString().split("T")[0]
datePicker.setAttribute("min", today)

timerTitle = forms[1].querySelector(".timer-name")
timerElements = forms[1].querySelectorAll("span")
firstDistance = 0
sec = 1000
minute = sec * 60
hour = minute *60
day = hour *24

function updateDom() {
    timerActive = setInterval(() =>{
        // if (shouldReset) {
        //
        // }
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
    console.log(inputTitle,inputDate )
    if (inputDate==='') {
        alert(`Please select a date for the Timer\nTimer name : "${inputTitle}"`)
    }else {
        inputValue = new Date(inputDate).getTime()
        timerTitle.textContent = `${inputTitle}`
        updateDom()
    }

}
function reset(){
    forms[0].hidden = false
    forms[1].hidden = true
    clearInterval(timerActive)
    inputTitle = ""
    inputDate = ""

}
forms[0].addEventListener("submit", updateCountdown)
forms[1].querySelectorAll(".timer-button")[1].addEventListener('click',reset)
forms[1].querySelectorAll(".timer-button")[0].addEventListener('click',() => {
    if (isPaused){
        isPaused=false
        forms[1].querySelectorAll("img")[0].setAttribute("src","./img/svg/pause.svg")
    } else {
        isPaused=true
        forms[1].querySelectorAll("img")[0].setAttribute("src","./img/svg/play.svg")
    }
})