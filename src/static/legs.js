const STAND_BUTTON = document.getElementById('stand-button');
const CROUCH_BUTTON = document.getElementById('crouch-button');

function standUp() {
    webSocket.send('{"l":1}');
}

function crouchDown() {
    webSocket.send('{"l":0}');
}

let standing = false;

registerListener(
    data => {
        standing = data['l'];
        if (standing !== undefined) {
            STAND_BUTTON.disabled = standing;
            CROUCH_BUTTON.disabled = !standing;
        }
    }
);

document.addEventListener('keydown', event => {
    if(event.key === " ") {
        event.preventDefault();
        if(standing) {
            crouchDown();
        } else {
            standUp();
        }
    }
});
