webSocket.onopen = () => webSocket.send('{"catchup":1}');
window.onload = () => webSocket.send('{"catchup":1}');
