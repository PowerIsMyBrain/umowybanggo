const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const audioElement = document.getElementById('audioElement');

let mediaRecorder;
let chunks = [];

startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = function (event) {
            chunks.push(event.data);
        }
        mediaRecorder.onstop = function () {
            const blob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
            const audioUrl = URL.createObjectURL(blob);
            audioElement.src = audioUrl;
        }
        mediaRecorder.start();
        startButton.disabled = true;
        stopButton.disabled = false;
    } catch (error) {
        console.error('Error accessing microphone:', error);
    }
}

function stopRecording() {
    mediaRecorder.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
}
