// const BACK_IP = "0.0.0.0"
// const BACK_PORT = 8080
// const baseUrl = `http://${BACK_IP}:${BACK_PORT}`

// // add Timer
// async function addTimer(timerName, durationInSeconds) {
//     token = sessionStorage.getItem('access_token')
//     const response = await fetch("{{baseUrl}}/timers/add", {
//         method: "POST",
//         credentials: "include",
//         headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
//         body: JSON.stringify({
//             name: timerName,
//             duration_seconds: durationInSeconds
//         })
//     })
//     response = response.json()
//     console.log(json);
// }

// async function stopTimer(timerName) {
//     token = sessionStorage.getItem('access_token')
//     const response = await fetch("{{baseUrl}}/timers/stop", {
//         method: "POST",
//         credentials: "include",
//         headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
//         body: JSON.stringify({
//             name: timerName
//         })
//     })
//     response = response.json()
//     console.log(json);

// }
// async function resumeTimer(timerName) {
//     token = sessionStorage.getItem('access_token')
//     const response = await fetch("{{baseUrl}}/timers/resume", {
//         method: "POST",
//         credentials: "include",
//         headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
//         body: JSON.stringify({
//             name: timerName
//         })
//     })
//         .then((response) => response.json())
//         .then((json) => console.log(json));

// }
// async function resetTimer(timerName, durationInSeconds) {
//     token = sessionStorage.getItem('access_token')
//     const response = await fetch("{{baseUrl}}/timers/reset", {
//         method: "POST",
//         credentials: "include",
//         headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
//         body: JSON.stringify({
//             name: timerName
//         })
//     })
//         .then((response) => response.json())
//         .then((json) => console.log(json));

// }
// async function removeTimer(timerName) {
//     token = sessionStorage.getItem('access_token')
//     const response = await fetch("{{baseUrl}}/timers/remove", {
//         method: "DELETE",
//         credentials: "include",
//         headers: { "Accept": "application/json", "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
//         body: JSON.stringify({
//             name: timerName
//         })
//     })
//         .then((response) => response.json())
//         .then((json) => console.log(json));
// }

