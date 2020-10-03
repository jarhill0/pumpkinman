const LISTENERS = [];

webSocket.onmessage = event => {
    const data = JSON.parse(event.data);
    LISTENERS.forEach(listener => listener(data));
}

function registerListener(listener) {
    LISTENERS.push(listener);
}
