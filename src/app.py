from json import dumps, loads

from quart import Quart, render_template, websocket

from relay_driver import RelayDriver

DRIVER = RelayDriver()
DRIVER.clear()

MOUTH = 0

app = Quart(__name__)


@app.route('/')
async def index():
    return await render_template('index.html')


@app.websocket("/ws")
async def ws():
    while True:
        data = await websocket.receive()
        try:
            order = loads(data)
        except ValueError:
            continue
        mouth = order.get('m')
        if mouth is not None:
            DRIVER[MOUTH] = mouth
            await websocket.send(dumps({'m': bool(mouth)}))


if __name__ == '__main__':
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
        )
    finally:
        DRIVER.stop()
