import json
import boto3
import gzip
from datetime import datetime
import base64
from botocore.exceptions import ClientError

# Initialize the S3 client
s3 = boto3.client('s3')

bucket_name = 'carras-real-time-data-processing-project'

# File path generator (groups files by minute)
def generate_s3_filename():
    current_time = datetime.utcnow().strftime('%Y-%m-%d_%H-%M')
    return f"raw/streaming/streaming_data_{current_time}.json.gz"

def read_existing_s3_file(bucket_name, key):
    """
    Reads and decompresses existing GZIP file from S3, if it exists.
    Returns the file content as a string.
    """
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        gz_data = response['Body'].read()
        return gzip.decompress(gz_data).decode('utf-8')
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            # File does not exist, return empty string
            return ""
        else:
            raise e

def lambda_handler(event, context):
    """
    AWS Lambda function to process Kinesis records, append to an existing file in S3, and store as NDJSON.
    """
    # List to hold JSON strings for NDJSON format
    records_data = []
    
    # Process all records from the event
    for record in event['Records']:
        try:
            # Decode and parse the Kinesis payload
            payload = base64.b64decode(record['kinesis']['data'])
            data = json.loads(payload)
            # Convert to JSON string and append to the list
            records_data.append(json.dumps(data))
        except Exception as e:
            print(f"Error processing record: {e}")
            continue

    # If records exist, append to the existing file in S3
    if records_data:
        try:
            # Generate the S3 file name
            filename = generate_s3_filename()
            
            # Read existing file (if it exists)
            existing_data = read_existing_s3_file(bucket_name, filename)
            
            # Combine existing data with new records
            combined_data = existing_data + "\n".join(records_data) + "\n"
            
            # Compress the combined NDJSON data
            gz_buffer = gzip.compress(combined_data.encode('utf-8'))
            
            # Upload the updated file to S3
            s3.put_object(
                Bucket=bucket_name,
                Key=filename,
                Body=gz_buffer,
                ContentType="application/json",
                ContentEncoding="gzip"
            )
            
            print(f"Successfully appended {len(records_data)} records to {filename}")
        
        except Exception as e:
            print(f"Error writing to S3: {e}")
            raise e

    return {"statusCode": 200, "body": f"Processed {len(records_data)} records."}
