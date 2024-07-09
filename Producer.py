import requests
from kafka import KafkaProducer
import json
import time

# Function to retrieve data from the API
def fetch_data(api_key):
    url = f'https://apiv2.allsportsapi.com/football/?met=Livescore&APIkey={api_key}'
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Function to create a Kafka producer
def create_producer():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',  # Kafka container address
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialization method for message values
    )
    return producer

# Function to send messages to Kafka
def send_messages(producer, topic, data):
    try:
        if data['success'] == 1:
            for event in data['result']:
                producer.send(topic, value=event)
                print(f"Sent: {event}")
                time.sleep(1)  # Sleep for 1 second between sends
        else:
            print("No successful data to send.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.flush()
        producer.close()

if __name__ == '__main__':
    API_KEY = '7f2a4b0e9e8f0aaa556e50295f047d137f05982cf576327262b0c9efa7c4b1a2'
    TOPIC = 'football_live'

    # Fetch data from API
    data = fetch_data(API_KEY)

    # Create Kafka producer
    producer = create_producer()

    # Send messages to Kafka
    send_messages(producer, TOPIC, data)
