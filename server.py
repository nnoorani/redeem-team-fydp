from flask import Flask, render_template, url_for, jsonify
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

database = {
    "6820020094" : {"name": "Chocolate Milk", "img-url": "products/chocolate-milk.jpg", "price": "3"},
    "06741806" : {"name": "Fanta", "img-url": "products/triscuit.jpg", "price": 1},
    "06782900" : {"name": "Coca-Cola", "img-url": "products/coke.jpg", "price": 1},
}

@app.route("/")
def index():
    return render_template('index.html',)

def handle_new_detection(barcode): 
	print "hello"
	print (barcode)
	data = construct_product_data(barcode)
	socketio.emit('new product', data)

@socketio.on('my event')
def handle_message(data):
	print (data)
	handle_new_detection("06741806")

def construct_product_data(barcode):
	return database[barcode]

if __name__ == "__main__":
    socketio.run(app)