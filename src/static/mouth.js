const mouthButton = document.getElementById('mouth-button')

let mouthOpen = false;

function openMouth() {
    webSocket.send('{"m":1}');
    mouthOpen = true;
}

function closeMouth() {
    webSocket.send('{"m":0}');
    mouthOpen = false;
}

registerListener(
    data => {
        const mouthOpen = data['m'];
        if (mouthOpen !== undefined) {
            mouthButton.style.backgroundColor = mouthOpen ? 'red' : '';
        }
    }
);
