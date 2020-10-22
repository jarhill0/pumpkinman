function registerTouchOn(element, handler) {
    element.touchOnHandler = handler;
    element.addEventListener("touchstart", startHandler, false);
    element.addEventListener("touchmove", moveOnHandler, false)
}

function registerTouchOff(element, handler) {
    element.touchOffHandler = handler;
    element.addEventListener("touchend", endHandler, false);
    element.addEventListener("touchcancel", cancelHandler, false);
    element.addEventListener("touchmove", moveOffHandler, false);
}

function moveOnHandler(event) {
    event.currentTarget.innerText = event.targetTouches.length;
}

const startHandler = moveOnHandler;
const endHandler = moveOnHandler;
const cancelHandler = moveOnHandler;
const moveOffHandler = moveOnHandler;
