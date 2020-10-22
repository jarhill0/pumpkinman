const HEAD_LIGHT_BOX = document.getElementById('head-light');

function headLight() {
    if (HEAD_LIGHT_BOX.checked) {
        webSocket.send('{"hl":1}');
    } else  {
        webSocket.send('{"hl":0}');
    }
}

registerListener(
    data => {
        const headLightOn = data['hl'];
        if (headLightOn !== undefined) {
            HEAD_LIGHT_BOX.checked = headLightOn;
        }
    }
);
