import boto3
import json
import time
from datetime import datetime, timezone
from botocore.exceptions import ClientError

#QUEUE_URL = "https://sqs.us-east-2.amazonaws.com/145023112744/email-processing-queue"


BUCKET_NAME = "eden-devops-s3"
REGION = "us-east-2"

sqs = boto3.client("sqs", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)

def get_token_from_ssm(token_name):
    ssm = boto3.client("ssm", region_name="us-east-2")
    response = ssm.get_parameter(
        Name=token_name,
        WithDecryption=True
    )
    return response["Parameter"]["Value"]

SQS_QUEUE_URL = get_token_from_ssm("sqs_queue_url_parameter")

def object_exists(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

def process_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        messages = response.get("Messages", [])

        if not messages:
            print("No messages in queue. Sleeping...")
            time.sleep(5)
            continue

        for message in messages:
            message_id = message["MessageId"]
            body = message["Body"]

            filename = f"email_{message_id}.json"

            if object_exists(BUCKET_NAME, filename):
                print(f"Message {message_id} already processed. Skipping.")
                continue

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=filename,
                Body=body
            )

            print(f"Saved message to S3 as {filename}")

        time.sleep(5)

if __name__ == "__main__":
    process_messages()
