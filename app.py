from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer
import threading
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Temporary storage for consumed messages
consumed_messages = []

# Kafka setup
consumer = KafkaConsumer(
    'football_live_clean',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def consume_kafka():
    global consumed_messages
    for message in consumer:
        data = message.value
        consumed_messages.append(data)
        socketio.emit('new_data', data)
        print(f"Sent: {data}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initial_data')
def initial_data():
    return jsonify(consumed_messages)

if __name__ == '__main__':
    kafka_thread = threading.Thread(target=consume_kafka)
    kafka_thread.daemon = True
    kafka_thread.start()
    socketio.run(app, debug=True)
