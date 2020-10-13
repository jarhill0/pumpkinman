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

CONNECTIONS = set()
RECORDINGS = deque(maxlen=16)
PLAYERS = dict()

app = Quart(__name__)


@app.route("/")
async def index():
    return await render_template("index.html")


@app.websocket("/ws")
async def ws():
    my_queue = Queue()
    CONNECTIONS.add(my_queue)
    try:
        recorder = Recorder()

        async def consumer():
            while True:
                order = await websocket.receive_json()
                await handle_state_change(order, websocket=websocket, recorder=recorder)

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


async def handle_state_change(change, websocket=None, recorder=None):
    mouth = change.get("m")
    if mouth is not None:
        mouth = bool(mouth)
        DRIVER[MOUTH] = mouth

        if recorder:
            recorder.take({"m": mouth})
        await broadcast({"m": mouth})

    if recorder:
        record = change.get("record")
        if record == "start" and not recorder.recording:
            recorder.start()
            await websocket.send_json({"record": True})
        elif record == "stop" and recorder.recording:
            recording_id = save_recording(recorder.stop())
            await websocket.send_json({"recording_id": recording_id})


@app.route("/admin", methods=["GET"])
async def admin_page():
    return await render_template("admin.html", revision=get_revision())


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
