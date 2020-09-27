let mouthOpen = false;

function openMouth() {
    webSocket.send('{"m":1}');
    mouthOpen = true;
}

function closeMouth() {
    webSocket.send('{"m":0}');
    mouthOpen = false;
}
