const UP_ARROW = document.getElementById('up-arrow');
const DOWN_ARROW = document.getElementById('down-arrow');
const LEFT_ARROW = document.getElementById('left-arrow');
const RIGHT_ARROW = document.getElementById('right-arrow');
const ARROWS = {u: UP_ARROW, d: DOWN_ARROW, l: LEFT_ARROW, r: RIGHT_ARROW};

function moveHead(where) {
    webSocket.send(`{"h":"${where}"}`);
}

registerListener(
    data => {
        const headPlace = data['h'];
        if (headPlace !== undefined) {
            for (const [key, element] of Object.entries(ARROWS)) {
                element.style.backgroundColor = key === headPlace ? 'red' : '';
            }
        }
    }
);

const KEY_MEANINGS = {ArrowUp: 'u', ArrowDown: 'd', ArrowLeft: 'l', ArrowRight: 'r'}

document.addEventListener('keydown', event => {
    const meaning = KEY_MEANINGS[event.key];
    if (meaning !== undefined) {
        event.preventDefault();
        moveHead(meaning);
    }
});
