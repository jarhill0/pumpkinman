const thresholdElement = document.getElementById('threshold');
const mouthButton = document.getElementById('mouth-button')

let audioStarted = false;
let recorder = null;
let peakMeter = null;
let meterNodeRaw = null;
let threshold = -19;


function startAudio() {
    if (audioStarted)
        return;

    if (!recorder)
        recorder = new RecorderService();
    if (!peakMeter)
        peakMeter = new WebAudioPeakMeter();
    recorder.onGraphSetupWithInputStream = (inputStreamNode) => {
      meterNodeRaw = peakMeter.createMeterNode(inputStreamNode, recorder.audioCtx)
      peakMeter.createMeter(document.getElementById('recording-meter'), meterNodeRaw, {}, takeAmplitude)
    }

    threshold = parseInt(thresholdElement.value, 10);
    thresholdElement.disabled = true;
    recorder.startRecording();
    audioStarted = true;
}

function stopAudio() {
    audioStarted = false;
    thresholdElement.disabled = false;
    document.getElementById('recording-meter').innerText = '';
    recorder.stopRecording();
}

let lastProcessed = 0;
const buffer = []
function takeAmplitude(amplitude) {
    buffer.push(amplitude);
    if (Date.now() - lastProcessed < 100) // process at most 10x/sec
        return;
    lastProcessed = Date.now();

    let votes = 0;
    while (buffer.length > 0) {
        if (buffer.pop() > threshold)
            votes++;
        else
            votes--;
    }
    if (votes > 0) {
        mouthButton.style.backgroundColor= "red"
        return openMouth();
    }
    mouthButton.style.backgroundColor= "";
    return closeMouth();
}
