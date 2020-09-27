const thresholdElement = document.getElementById('threshold');
const mouthButton = document.getElementById('mouth-button')
const increasingElement = document.getElementById('increasing-box')

let audioStarted = false;
let requireIncreasing = false;
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
    requireIncreasing = increasingElement.checked;
    increasingElement.disabled = true;
    recorder.startRecording();
    audioStarted = true;
}

function stopAudio() {
    audioStarted = false;
    thresholdElement.disabled = false;
    increasingElement.disabled = false;
    document.getElementById('recording-meter').innerText = '';
    recorder.stopRecording();
}

let last = 0;
function takeAmplitude(amplitude) {
    if (amplitude > threshold && (!requireIncreasing || amplitude > last)) {
        last = amplitude
        mouthButton.style.backgroundColor = "red";
        return openMouth()
    }
    last = amplitude
    mouthButton.style.backgroundColor = "";
    return closeMouth();
}
