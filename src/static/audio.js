const thresholdElement = document.getElementById('threshold');
const mouthButton = document.getElementById('mouth-button')
const increasingElement = document.getElementById('increasing-box')
const openTimeElement = document.getElementById('min-open-time')

let audioStarted = false;
let requireIncreasing = false;
let recorder = null;
let peakMeter = null;
let meterNodeRaw = null;
let threshold = -19;
let minOpenTime = 0;


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
    minOpenTime = parseInt(openTimeElement.value, 10);
    openTimeElement.disabled = true;
    requireIncreasing = increasingElement.checked;
    increasingElement.disabled = true;
    recorder.startRecording();
    audioStarted = true;
}

function stopAudio() {
    audioStarted = false;
    thresholdElement.disabled = false;
    increasingElement.disabled = false;
    openTimeElement.disabled = false;
    document.getElementById('recording-meter').innerText = '';
    recorder.stopRecording();
}

let last = 0;
let lastRisingEdge = 0;
function takeAmplitude(amplitude) {
    if (amplitude > threshold && (!requireIncreasing || amplitude > last)) {
        last = amplitude
        if (!mouthOpen)
            lastRisingEdge = Date.now();
        mouthButton.style.backgroundColor = "red";
        return openMouth()
    }
    last = amplitude

    if (Date.now() - lastRisingEdge < minOpenTime)
        return;

    mouthButton.style.backgroundColor = "";
    return closeMouth();
}
