const startButton = document.getElementById('startRecordingButton');
const stopButton = document.getElementById('stopRecordingButton')

function startRecording() {
    webSocket.send('{"record":"start"}')
    startButton.disabled = true;
    stopButton.disabled = false;
}

function stopRecording() {
    webSocket.send('{"record":"stop"}')
    startButton.disabled = false;
    stopButton.disabled = true;
}

function download(path) {
    window.open(path);
}

registerListener(
    data => {
        const recording_id = data['recording_id'];
        if (recording_id !== undefined) {
            download(recordingBaseUrl.replace('REPLACEME', recording_id));
        }
    }
);
