import json
from pyspark import SparkContext
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient

# Configuration de MongoDB
client = MongoClient('localhost', 27017)
db = client['FootballDB']
collection = db['LiveMatchData']

def structure_validate_data(msg):
    data_dict = {}

    # Parser le message
    event = json.loads(msg.value.decode("utf-8"))

    data_dict["RawData"] = event

    # Valider et structurer les données
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

    # Ajouter d'autres champs si nécessaire...

    return data_dict

sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")

# Configuration de Kafka
consumer = KafkaConsumer(
    'football_live', 
    auto_offset_reset='earliest', 
    bootstrap_servers=['localhost:9092'], 
    consumer_timeout_ms=1000
)
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

for msg in consumer:
    if msg.value.decode("utf-8") != "Error in Connection":
        data = structure_validate_data(msg)
        
        # Remplacer le document existant ou insérer s'il n'existe pas
        result = collection.replace_one(
            {'event_key': data['event_key']},
            data,
            upsert=True
        )
        
        # Si un document a été mis à jour ou inséré, l'envoyer au topic 'football_live_clean'
        if result.matched_count > 0 or result.upserted_id is not None:
            # Ajouter l'ID du document MongoDB aux données avant de les envoyer
            if result.upserted_id:
                data["_id"] = str(result.upserted_id)
            else:
                existing_doc = collection.find_one({'event_key': data['event_key']})
                data["_id"] = str(existing_doc['_id'])

            producer.send("football_live_clean", json.dumps(data).encode('utf-8'))
        
        print(data)
