import requests
from kafka import KafkaProducer
import json
import time
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

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
                print(f"Sent to Kafka: {event}")
                time.sleep(1)  # Sleep for 1 second between sends
        else:
            print("No successful data to send.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.flush()

# Function to insert data into MongoDB
def insert_to_mongo(db, data):
    try:
        if data['success'] == 1:
            for event in data['result']:
                event['_id'] = str(ObjectId())  # Convert ObjectId to string
                db.insert_one(event)
        else:
            print("No successful data to insert.")
    except Exception as e:
        print(f"An error occurred while inserting to MongoDB: {e}")

if __name__ == '__main__':
    API_KEY = os.getenv('API_KEY')
    TOPIC = 'football_live'

    # Create Kafka producer
    producer = create_producer()

    # MongoDB setup
    client = MongoClient('localhost', 27017)
    db = client['FootballDB']['RawData']

    while True:
        try:
            # Fetch data from API
            data = fetch_data(API_KEY)

            # Insert data into MongoDB
            insert_to_mongo(db, data)

            # Send messages to Kafka
            send_messages(producer, TOPIC, data)
            
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(60)  # Wait for 60 seconds before fetching new data
