import asyncio
import sys
sys.path.append("/home/ubuntu/AIC_Inference/AICpackages")
from readdata import run
from celery import Celery
import boto3
import time
from dotenv import load_dotenv
import os
import time

load_dotenv(".credentials")

kinesis = boto3.client("kinesis", 
                        aws_access_key_id=os.getenv("ACCESS_KEY"),
                        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                        region_name="ap-southeast-1")
streams_processing = []

def main():
    print("App starting...")
    while True:
        streams_get = kinesis.list_streams()["StreamNames"]

        for name in streams_get:
            info = kinesis.describe_stream_summary(StreamName=name)
            status = info["StreamDescriptionSummary"]["StreamStatus"]
            if status == "ACTIVE" and not '_inference' in name and name not in streams_processing:
                streams_processing.append(name)
                run.delay(name)
                print(f"DataStream active on {name}...")
        
        time.sleep(10)


if __name__ == "__main__":
    main()