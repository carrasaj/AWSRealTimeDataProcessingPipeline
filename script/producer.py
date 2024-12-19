import boto3
import json
import time
import random
from datetime import datetime

# Initialize the Kinesis client
kinesis = boto3.client('kinesis', region_name='us-east-1')

# Function to generate log records
def generate_log_record():
    # Generate a single record as a dictionary
    return {
        "timestamp": datetime.utcnow().isoformat(),  # ISO 8601 format (e.g., "2024-12-18T15:45:00.123Z")
        "device_id": f"device-{random.randint(1, 100)}",
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(30, 50), 2)
    }

# Infinite loop to simulate real-time data streaming
while True:
    # Generate one record
    record = generate_log_record()

    # Convert the dictionary to a JSON string
    record_str = json.dumps(record)

    # Send the JSON object to the Kinesis stream
    kinesis.put_record(
        StreamName='my-streaming-logs',
        Data=record_str,
        PartitionKey=str(record["device_id"])
    )

    # Log the record to the console for debugging
    print(f"Sent record: {record}")

    # Sleep for 1 second to simulate real-time data generation
    time.sleep(1)
