import json
import uuid
import psycopg2
from kafka import KafkaConsumer
import os

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# PostgreSQL connection setup
DB_CONFIG = {
    "dbname": "ecommerce",
    "user": db_user,
    "password": db_password,
    "host": db_host,
    "port": "5432",
}

# Kafka consumer setup
KAFKA_BROKER = "localhost:9092"
TOPICS = ["user_activity_events", "user_transaction_events"]

consumer = KafkaConsumer(
    *TOPICS,
    bootstrap_servers=KAFKA_BROKER,
    group_id="ecommerce-group",  # Track processed messages
    auto_offset_reset="earliest",  # Start from the beginning
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

# Database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Insert data based on event type
def process_event(event):
    conn = get_db_connection()
    cur = conn.cursor()

    event_name = event.get("event_name")
    event_id = event.get("event_id", str(uuid.uuid4()))
    timestamp = event.get("timestamp")

    try:
        if event_name in ["page_view", "click"]:
            # Insert into users
            cur.execute(
                "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING",
                (event["event_properties"]["user_id"],),
            )
            # Insert into events
            cur.execute(
                "INSERT INTO events (event_id, event_name, event_type, created_at) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (event_id, event_name, "action", event["event_properties"]["timestamp"]),
            )
            # Insert into page_views or clicks
            if event_name == "page_view":
                cur.execute(
                    f"INSERT INTO page_views (page_view_id, user_id, path, timestamp, event_id) VALUES (%s, %s, %s, %s, %s)",
                    (str(uuid.uuid4()), event["event_properties"]["user_id"], event["path"], event["event_properties"]["timestamp"], event_id),
                )
            elif event_name == "click":
                cur.execute(
                    f"INSERT INTO clicks (click_id, user_id, path, timestamp, event_id) VALUES (%s, %s, %s, %s, %s)",
                    (str(uuid.uuid4()), event["event_properties"]["user_id"], event["path"], event["event_properties"]["timestamp"], event_id),
                )

        elif event_name == "purchase":
            # Insert into users if not exists
            cur.execute(
                "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING",
                (event["user_id"],),
            )
            # Insert into events
            cur.execute(
                "INSERT INTO events (event_id, event_name, event_type, created_at) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (event_id, "purchase", "transaction", timestamp),
            )
            # Insert into transactions
            cur.execute(
                "INSERT INTO transactions (transaction_id, user_id, transaction_amount, timestamp, event_id) VALUES (%s, %s, %s, %s, %s)",
                (str(uuid.uuid4()), event["user_id"], event["transaction_amount"], timestamp, event_id),
            )

        conn.commit()
    except Exception as e:
        print(f"Error inserting event: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# Start consuming messages
print("Consumer is running...")
for msg in consumer:
    process_event(msg.value)
