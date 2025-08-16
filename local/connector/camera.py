import cv2
import boto3
import os
import base64
import json
import time
from dotenv import load_dotenv
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor

load_dotenv("../.credentials")

class Camera:
    def __init__(self, id, stream_name, partkey, location):
        config = Config(
            max_pool_connections=50,
            retries={'max_attempts': 3}
        )
        self.video = cv2.VideoCapture(int(id))
        self.kinesis = boto3.client("kinesis", 
                                aws_access_key_id=os.getenv("ACCESS_KEY"),
                                aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                                region_name="ap-southeast-1",
                                config=config)
        self.stream_name = stream_name
        self.partkey = partkey
        self.location = location

        self.pool = ThreadPoolExecutor(max_workers=40)

    
    def compress_and_base64(self, frame, quality=80, max_width=1000):
        h, w = frame.shape[:2]
        if w > max_width:
            ratio = max_width / float(w)
            frame = cv2.resize(frame, (max_width, int(h * ratio)))
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        return base64.b64encode(buffer).decode('utf-8')

    def camera(self):
        _, frame = self.video.read()

        img_base64 = self.compress_and_base64(frame)

        payload = {
            "origin": self.stream_name,
            "location": self.location,
            "image_data": img_base64,
            "time_stamp": time.time()
        }


        json_data = json.dumps(payload)
        self.pool.submit(self.send_to_kinesis, json_data)
    
    def send_to_kinesis(self, json_data):
        self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=json_data.encode("utf-8"),
            PartitionKey=self.partkey
        )