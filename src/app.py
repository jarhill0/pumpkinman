from collections import deque
from json import dumps, loads
from random import choices
from string import ascii_letters

from quart import Quart, make_response, render_template, websocket

from recordings import Recorder
from relay_driver import RelayDriver

DRIVER = RelayDriver()
DRIVER.clear()

MOUTH = 0

RECORDINGS = deque(maxlen=16)

app = Quart(__name__)


@app.route('/')
async def index():
    return await render_template('index.html')


@app.websocket("/ws")
async def ws():
    recorder = Recorder()
    while True:
        data = await websocket.receive()
        try:
            order = loads(data)
        except ValueError:
            continue
        mouth = order.get('m')
        if mouth is not None:
            mouth = bool(mouth)
            recorder.take({'m': mouth})
            DRIVER[MOUTH] = mouth
            await websocket.send(dumps({'m': mouth}))

        record = order.get('record')
        if record == 'start' and not recorder.recording:
            recorder.start()
            await websocket.send(dumps({'record': True}))
        elif record == 'stop' and recorder.recording:
            recording_id = save_recording(recorder.stop())
            await websocket.send(dumps({'recording_id': recording_id}))


@app.route('/recording/<identifier>', methods=['GET'])
async def download_recording(identifier):
    recording = lookup_recording(identifier)
    if recording:
        resp = await make_response(recording)
        resp.headers['Content-Type'] = 'application/octet-stream'
        resp.headers['Content-Disposition'] = f'attachment; filename="{identifier}.rec"'
        return resp
    return "Couldn't find that recording!", 404


def save_recording(recording):
    identifier = ''.join(choices(ascii_letters, k=5))
    RECORDINGS.append((identifier, recording))
    return identifier


def lookup_recording(identifier):
    return next((rec for ident, rec in RECORDINGS if ident == identifier), None)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        DRIVER.stop()
