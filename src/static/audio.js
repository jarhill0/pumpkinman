const thresholdElement = document.getElementById('threshold');

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
function takeAmplitude(amplitude) {
    if (Date.now() - lastProcessed < 100) // process at most 10x/sec
        return;
    lastProcessed = Date.now();

    if (amplitude > threshold)
        return openMouth();
    return closeMouth();
}
