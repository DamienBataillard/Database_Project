from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Fonction pour nettoyer les données
def clean_data(data):
    cleaned_data = {
        "event_id": data.get("event_key"),
        "event_date": data.get("event_date"),
        "event_time": data.get("event_time"),
        "home_team": data.get("event_home_team"),
        "away_team": data.get("event_away_team"),
        "score_home": data.get("event_final_result").split("-")[0].strip() if data.get("event_final_result") else None,
        "score_away": data.get("event_final_result").split("-")[1].strip() if data.get("event_final_result") else None,
        "country": data.get("country_name"),
        "league": data.get("league_name"),
        "goalscorers": data.get("goalscorers", []),
        "substitutes": data.get("substitutes", []),
        "cards": data.get("cards", []),
        "statistics": data.get("statistics", [])
    }
    return cleaned_data

# Fonction pour créer un consommateur Kafka
def create_consumer(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

# Fonction pour insérer des données dans MongoDB
def insert_into_mongodb(collection, data):
    try:
        collection.insert_one(data)
        print(f"Inserted: {data}")
    except Exception as e:
        print(f"An error occurred while inserting data into MongoDB: {e}")

if __name__ == '__main__':
    TOPIC = 'football_live'
    
    # Connexion à MongoDB
    client = MongoClient('localhost', 27017)
    db = client['footreel']
    collection = db['live_scores']

    # Créer un consommateur Kafka
    consumer = create_consumer(TOPIC)

    # Lire les messages de Kafka, nettoyer et insérer dans MongoDB
    for message in consumer:
        data = message.value
        cleaned_data = clean_data(data)
        insert_into_mongodb(collection, cleaned_data)
