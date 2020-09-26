from flask import Flask, render_template, request

from relay_driver import RelayDriver

DRIVER = RelayDriver()
DRIVER.clear()

MOUTH = 0

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mouth', methods=['POST'])
def mouth():
    state = request.values.get('state')
    if state is None:
        return 'Could not find mandatory `state` parameter.', 422
    state = bool(state)
    DRIVER[0] = state
    return f'{"Opened" if state else "Closed"} mouth.'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
