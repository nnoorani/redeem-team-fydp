
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from flask import Flask, render_template, url_for, jsonify
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

database = {
    "6820020094" : {"name": "Chocolate Milk", "img-url": "products/chocolate-milk.jpg", "price": "3"},
    "06741806" : {"name": "Fanta", "img-url": "products/triscuit.jpg", "price": 1},
    "06782900" : {"name": "Coca-Cola", "img-url": "products/coke.jpg", "price": 1},
}

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        print "helllooooooooo"
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

@app.route("/")
def index():
    # return render_template('index.html')

def start_server():
    socketio.run(app)
>>>>>>> d5c8300... updated interface working state
