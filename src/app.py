from asyncio import Queue, ensure_future, gather
from collections import deque
from os import system
from random import choices
from string import ascii_letters
import subprocess

from quart import Quart, make_response, render_template, request, websocket

from recordings import Player, Recorder
from relay_driver import RelayDriver

DRIVER = RelayDriver()
DRIVER.clear()

MOUTH = 0
ARMS = 1
LEFT_HEAD = 2
RIGHT_HEAD = 3
HEAD_LIGHT = 4
LEGS = 5
FOG = 6

BODY_STATE = dict()

CONNECTIONS = set()
RECORDINGS = deque(maxlen=16)
PLAYERS = dict()

app = Quart(__name__)


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/relays")
async def relays():
    return await render_template("relays.html")


@app.websocket("/ws")
async def ws():
    my_queue = Queue()
    CONNECTIONS.add(my_queue)
    try:
        recorder = Recorder()

        async def consumer():
            while True:
                order = await websocket.receive_json()
                await handle_order(order, websocket, recorder)

        async def producer():
            while True:
                data = await my_queue.get()
                await websocket.send_json(data)

        consumer_task = ensure_future(consumer())
        producer_task = ensure_future(producer())
        try:
            await gather(consumer_task, producer_task)
        finally:
            consumer_task.cancel()
            producer_task.cancel()
    finally:
        CONNECTIONS.remove(my_queue)


async def broadcast(message):
    for connection in CONNECTIONS:
        await connection.put(message)


async def handle_order(order, wbsckt, recorder):
    record = order.get("record")
    if record == "start" and not recorder.recording:
        recorder.start()
        await wbsckt.send_json({"record": True})
    elif record == "stop" and recorder.recording:
        recording_id = save_recording(recorder.stop())
        await wbsckt.send_json({"recording_id": recording_id})

    if order.get("catchup") is not None:
        await wbsckt.send_json(BODY_STATE)
        return

    change = sanitize(order)
    await handle_state_change(change)
    recorder.take(change)


async def handle_state_change(change):
    BODY_STATE.update(**change)
    apply(change)
    await broadcast(change)


def permit(d, keys):
    return {k: v for k, v in d.items() if k in keys}


def booleanize_keys(d, exclude=()):
    return {k: (v if k in exclude else bool(v)) for k, v in d.items()}


def sanitize(change):
    return booleanize_keys(permit(change, _ALLOWED_ACTIONS), exclude={"h"})


_HEAD_STATES = {
    "u": {LEFT_HEAD: True, RIGHT_HEAD: True},
    "d": {LEFT_HEAD: False, RIGHT_HEAD: False},
    "r": {LEFT_HEAD: True, RIGHT_HEAD: False},
    "l": {LEFT_HEAD: False, RIGHT_HEAD: True},
}


def set_head(state):
    setting = _HEAD_STATES.get(state)
    if setting:
        DRIVER.bulk_set(setting)


def relay_action(relay_num):
    def action(state):
        DRIVER[relay_num] = state

    return action


_ACTIONS = {
    "m": relay_action(MOUTH),
    "l": relay_action(LEGS),
    "a": relay_action(ARMS),
    "hl": relay_action(HEAD_LIGHT),
    "f": relay_action(FOG),
    "h": set_head,
    "0": relay_action(0),
    "1": relay_action(1),
    "2": relay_action(2),
    "3": relay_action(3),
    "4": relay_action(4),
    "5": relay_action(5),
    "6": relay_action(6),
    "7": relay_action(7),
}
_ALLOWED_ACTIONS = set(_ACTIONS.keys())


def apply(change):
    for name, state in change.items():
        handler = _ACTIONS.get(name)
        if handler:  # really shouldn't be None, but just in case??
            handler(state)


@app.route("/admin", methods=["GET"])
async def admin_page():
    return await render_template("admin.html", revision=REVISION)


@app.route("/gitpull", methods=["POST"])
async def git_pull():
    if system("git pull") == 0:
        return "Success"
    return "Failure", 422


@app.route("/reboot", methods=["POST"])
async def reboot():
    if system("sudo reboot") == 0:
        return "Success"
    return "Failure", 422


@app.route("/shutdown", methods=["POST"])
async def shutdown():
    if system("sudo shutdown -h now") == 0:
        return "Success"
    return "Failure", 422


def get_revision():
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")


REVISION = get_revision()


@app.route("/recording/<identifier>", methods=["GET"])
async def download_recording(identifier):
    recording = lookup_recording(identifier)
    if recording:
        resp = await make_response(recording)
        resp.headers["Content-Type"] = "application/octet-stream"
        resp.headers["Content-Disposition"] = f'attachment; filename="{identifier}.rec"'
        return resp
    return "Couldn't find that recording!", 404


@app.route("/recording/upload", methods=["POST"])
async def upload_recording():
    files = await request.files
    recording = files.get("recording")
    if not recording:
        return "No file!", 422
    identifier = "".join(choices(ascii_letters, k=20))
    try:
        PLAYERS[identifier] = Player(recording, handle_state_change)
    except Exception as e:
        return str(e), 422
    return await render_template("player.html", identifier=identifier)


@app.websocket("/ws_play/<identifier>")
async def ws_play(identifier):
    player = PLAYERS[identifier]
    try:
        command = None
        while True:
            if command is None:
                command = await websocket.receive()
            if command == "play":
                command = None

                async def look_for_stop():
                    nonlocal command
                    command = await websocket.receive()
                    if command == "stop":
                        player.stop()
                        command = None

                async def play():
                    await websocket.send("playing")
                    await player.play()
                    await websocket.send("stopped")

                play_task = ensure_future(play())
                stop_task = ensure_future(look_for_stop())
                try:
                    await gather(play_task, stop_task)
                finally:
                    play_task.cancel()
                    stop_task.cancel()
    finally:
        del PLAYERS[identifier]


def save_recording(recording):
    identifier = "".join(choices(ascii_letters, k=5))
    RECORDINGS.append((identifier, recording))
    return identifier


def lookup_recording(identifier):
    return next((rec for ident, rec in RECORDINGS if ident == identifier), None)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        DRIVER.stop()
