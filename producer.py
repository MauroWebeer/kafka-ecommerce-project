from confluent_kafka import Producer
import json
import time
import random
from datetime import datetime, timezone
import uuid

# Kafka Configuration
conf = {'bootstrap.servers': 'localhost:9092',
        'client.id': 'python-producer'
}
producer = Producer(conf)

# Function to generate a random event
def generate_event():
    topic = random.choice(["user_activity_events", "user_login_events", "user_transaction_events"])
    
    if topic == "user_activity_events":
        event = {
            "event_name": random.choice(["page_view", "click"]),
            "event_id": str(uuid.uuid4()),  # Generates a unique UUID
            "event_type": "action",
            "path": random.choice(["/home", "/product/123", "/cart", "/checkout"]),
            "event_properties": {
                "user_id": random.randint(1, 10000),  # Random user ID between 1 and 10,000
                "timestamp": datetime.now(timezone.utc).isoformat()  # Current UTC timestamp
            }
        }
    
    else:  # user_transaction_events
        event = {
            "event_name": "purchase",
            "event_id": str(uuid.uuid4()),  # Unique event ID
            "event_type": "transaction",
            "user_id": random.randint(10000, 99999),  # User ID between 10,000 and 99,999
            "transaction_amount": round(random.uniform(1.00, 1000.00), 2),  # Random float with 2 decimals
            "timestamp": datetime.now(timezone.utc).isoformat()  # Current UTC timestamp
        }
    
    return topic, event

# Function to send an event to Kafka
def send_event():
    topic, event = generate_event()
    event_json = json.dumps(event)
    producer.produce(topic, key=event["event_id"], value=event_json)
    producer.flush()
    
    print(f"Sent to {topic}: {event_json}")

# Simulate sending events every 2 seconds
while True:
    send_event()
    time.sleep(2)
