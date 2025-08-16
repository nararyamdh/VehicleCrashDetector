import boto3
import os
from dotenv import load_dotenv

def check_active(kinesis_name):
    load_dotenv("../.credentials")

    kinesis = boto3.client("kinesis", 
                            aws_access_key_id=os.getenv("ACCESS_KEY"),
                            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                            region_name="ap-southeast-1")
    
    response = kinesis.list_streams()

    if response.get("StreamNames"):
        if kinesis_name in response["StreamNames"]:
            return True
    
    return False