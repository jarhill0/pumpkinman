function activate(num) {
    webSocket.send(`{"${num}":1}`);
}

function deactivate(num) {
    webSocket.send(`{"${num}":0}`);
}

const statusIndicators = [];

for (let num = 0; num < 8; num++) {
    statusIndicators.push(document.getElementById(`status-${num}`));
}

const checkboxes = [];

for (let num = 0; num < 8; num++) {
    checkboxes.push(document.getElementById(`checkbox-${num}`));
}

document.querySelectorAll('.checkbox').forEach((checkbox, index) => {
        checkbox.addEventListener('change', event => {
            if (event.target.checked) {
                activate(index);
            } else {
                deactivate(index);
            }
        });
    }
);

document.addEventListener('keydown', event => {
    const number = parseInt(event.key, 10);
    if (1 <= number && number <= 8) {
        activate(number - 1)
    }
});

document.addEventListener('keyup', event => {
    const number = parseInt(event.key, 10);
    if (1 <= number && number <= 8) {
        deactivate(number - 1)
    }
});

registerListener(
    data => {
        for (let num = 0; num < 8; num++) {
            const activated = data[num.toFixed(0)];
            if (activated !== undefined) {
                statusIndicators[num].style.backgroundColor = activated ? 'red' : '';
                checkboxes[num].checked = activated;
            }
        }
    }
);
