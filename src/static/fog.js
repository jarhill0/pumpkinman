const FOG_BOX = document.getElementById('fog');

function fog() {
    if (FOG_BOX.checked) {
        webSocket.send('{"f":1}');
    } else  {
        webSocket.send('{"f":0}');
    }
}

document.addEventListener('keydown', event => {
    if(event.key === "f") {
        event.preventDefault();
        FOG_BOX.checked = !FOG_BOX.checked
        fog();
    }
});

registerListener(
    data => {
        const fogOn = data['f'];
        if (fogOn !== undefined) {
            FOG_BOX.checked = fogOn;
        }
    }
);
