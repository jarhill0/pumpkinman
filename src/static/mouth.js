function openMouth() {
    return fetch(OPEN_URL, {method: 'POST'});
}

function closeMouth() {
    return fetch(CLOSE_URL, {method: 'POST'});
}