from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer
import threading
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Temporary storage for consumed messages, using a dictionary to avoid duplicates
consumed_messages = {}
emitted_event_keys = set()

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
        event_key = data.get('event_key')

        if event_key:
            if event_key in consumed_messages:
                # If the message exists, check if it needs updating
                if consumed_messages[event_key] != data:
                    consumed_messages[event_key] = data
                    if event_key not in emitted_event_keys:
                        socketio.emit('new_data', data)
                        emitted_event_keys.add(event_key)
                    print(f"Updated and sent: {data}")
            else:
                # If the message does not exist, add it
                consumed_messages[event_key] = data
                if event_key not in emitted_event_keys:
                    socketio.emit('new_data', data)
                    emitted_event_keys.add(event_key)
                print(f"Added and sent: {data}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initial_data')
def initial_data():
    # Return the list of unique messages
    return jsonify(list(consumed_messages.values()))

if __name__ == '__main__':
    kafka_thread = threading.Thread(target=consume_kafka)
    kafka_thread.daemon = True
    kafka_thread.start()
    socketio.run(app, debug=True)
