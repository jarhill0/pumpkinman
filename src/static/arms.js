const ARMS_UP_BUTTON = document.getElementById('arms-up-button');
const ARMS_DOWN_BUTTON = document.getElementById('arms-down-button');

function armsUp() {
    webSocket.send('{"a":1}');
}

function armsDown() {
    webSocket.send('{"a":0}');
}

let armsAreUp = false;

registerListener(
    data => {
        const armState = data['a'];
        if (armState !== undefined) {
            armsAreUp = armState;
            ARMS_UP_BUTTON.disabled = armsAreUp;
            ARMS_DOWN_BUTTON.disabled = !armsAreUp;
        }
    }
);

document.addEventListener('keydown', event => {
    if(event.key === "a") {
        event.preventDefault();
        if(armsAreUp) {
            armsDown();
        } else {
            armsUp();
        }
    }
});
