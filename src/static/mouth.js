function openMouth() {
    webSocket.send('{"m":1}');
}

function closeMouth() {
    webSocket.send('{"m":0}');
}
