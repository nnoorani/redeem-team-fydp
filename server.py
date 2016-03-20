from flask import Flask, render_template, url_for, jsonify
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)
socketio.emit('new product', "la")

database = {
    "6820020094" : {"name": "Chocolate Milk", "img-url": "products/chocolate-milk.jpg", "price": "3"},
    "066721003140" : {"name": "Fanta", "img-url": "products/triscuit.jpg", "price": 1},
    "06782900" : {"name": "Coca-Cola", "img-url": "products/coke.jpg", "price": 1},
}

@app.route("/")
def index():
    return render_template('index.html',)

def handle_new_detection(barcode): 
	print "hello"
	print (barcode)
	data = construct_product_data(barcode)
	print data
	socketio.emit('new product', data, namespace="/")
	print "emitted the socket event"

@socketio.on('my event', namespace="/")
def handle_message(data):
	print (data)

def construct_product_data(barcode):
	return database[barcode]

def start_server():
	print "im starting the server"
	socketio.run(app)
