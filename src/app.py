from json import loads

from quart import Quart, render_template, request, websocket

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


@app.route('/mouth', methods=['POST'])
async def mouth():
    state = request.values.get('state')
    if state is None:
        return 'Could not find mandatory `state` parameter.', 422
    state = bool(state)
    DRIVER[0] = state
    return f'{"Opened" if state else "Closed"} mouth.'


if __name__ == '__main__':
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
        )
    finally:
        DRIVER.stop()
