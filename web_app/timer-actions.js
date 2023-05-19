const BACK_IP = "0.0.0.0"
const BACK_PORT = 8080
const baseUrl = `http://${BACK_IP}:${BACK_PORT}`

// add Timer
async function addTimer(timerName, durationInSeconds) {
    const response = await fetch("{{baseUrl}}/timers/add", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            name: timerName,
            duration_seconds: durationInSeconds
        })
    })
        .then((response) => response.json())
        .then((json) => console.log(json));
}

async function stopTimer(timerName) {
    const response = await fetch("{{baseUrl}}/timers/stop", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            name: timerName
        })
    })
        .then((response) => response.json())
        .then((json) => console.log(json));

}
async function resumeTimer(timerName) {
    const response = await fetch("{{baseUrl}}/timers/resume", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            name: timerName
        })
    })
        .then((response) => response.json())
        .then((json) => console.log(json));

}
async function resetTimer(timerName, durationInSeconds) {
    const response = await fetch("{{baseUrl}}/timers/reset", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            name: timerName
        })
    })
        .then((response) => response.json())
        .then((json) => console.log(json));

}
async function removeTimer(timerName) {
    const response = await fetch("{{baseUrl}}/timers/remove", {
        method: "DELETE",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
            name: timerName
        })
    })
        .then((response) => response.json())
        .then((json) => console.log(json));
}
