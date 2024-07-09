import json
from dateutil import parser
from pyspark import SparkContext
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client['FootballDB']
collection = db['LiveMatchData']

def event_key_exist(event_key):
    return collection.count_documents({'event_key': event_key}) > 0

def structure_validate_data(msg):
    data_dict = {}
    
    # Parse message
    event = json.loads(msg.value.decode("utf-8"))
    
    data_dict["RawData"] = event
    
    # Validate and structure data
    try:
        data_dict["event_key"] = event['event_key']
    except KeyError:
        data_dict["event_key"] = "Error"

    try:
        data_dict["event_date"] = event['event_date']
    except KeyError:
        data_dict["event_date"] = "Error"
    
    try:
        data_dict["event_time"] = event['event_time']
    except KeyError:
        data_dict["event_time"] = "Error"
    
    try:
        data_dict["event_home_team"] = event['event_home_team']
    except KeyError:
        data_dict["event_home_team"] = "Error"

    try:
        data_dict["event_away_team"] = event['event_away_team']
    except KeyError:
        data_dict["event_away_team"] = "Error"

    # Add more fields as needed...

    return data_dict

sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")

# Kafka setup
consumer = KafkaConsumer('football_live', auto_offset_reset='earliest', bootstrap_servers=['localhost:9092'], consumer_timeout_ms=1000)
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

for msg in consumer:
    if msg.value.decode("utf-8") != "Error in Connection":
        data = structure_validate_data(msg)
        
        if not event_key_exist(data['event_key']):
            # Push data to MongoDB
            result = collection.insert_one(data)
            # Convert ObjectId to string
            data["_id"] = str(result.inserted_id)
            producer.send("football_live_clean", json.dumps(data).encode('utf-8'))
        
        print(data)
