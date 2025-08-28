import json
import boto3
import random
import time
from datetime import datetime

kinesis_client = boto3.client('kinesis', region_name='us-east-1') 
STREAM_NAME = "clickstream-input"

def send_click_event():
    """Generates and sends a single click event to Kinesis."""
    event_data = {
        "event_id": f"evt-{random.randint(1000, 9999)}",
        "user_id": f"user-{random.choice(['a', 'b', 'c', 'd'])}",
        "event_type": random.choice(["page_view", "add_to_cart", "purchase"]),
        "url": f"/product/{random.randint(1, 50)}",
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        response = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(event_data),
            PartitionKey=event_data["user_id"]
        )
        print(f"Sent event {event_data['event_id']} to Kinesis. Sequence Number: {response['SequenceNumber']}")
    except Exception as e:
        print(f"Error sending data to Kinesis: {e}")

if __name__ == "__main__":
    print(f"Starting to send clickstream data to '{STREAM_NAME}'...")
    while True:
        send_click_event()
        time.sleep(1)
