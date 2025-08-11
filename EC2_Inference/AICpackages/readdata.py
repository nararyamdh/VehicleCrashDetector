import boto3
from dotenv import load_dotenv
import cv2
import numpy as np
import sys
sys.path.append("../processor")
from processor.inference import Detector
sys.path.append("../AICpackages")
from AICpackages.draw import draw
from AICpackages.sender import send_plain_image
import asyncio
import httpx
import io
import os
from PIL import Image

load_dotenv("../.credentials")

url = os.getenv("ACCESS_KEY")

timerStatus = False

async def timer():
    global timerStatus
    print("Timer berjalan...")
    timerStatus = True
    await asyncio.sleep(60*30)
    timerStatus = False

async def readdata(stream_name):
    kinesis = boto3.client("kinesis", 
                            aws_access_key_id=os.getenv("ACCESS_KEY"),
                            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                            region_name="ap-southeast-1")
    shards = kinesis.describe_stream(StreamName=stream_name)["StreamDescription"]["Shards"]
    shard_id = shards[0]["ShardId"]

    shard_iterator = kinesis.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType="LATEST"
    )["ShardIterator"]

    model = Detector()

    while True:
        response = kinesis.get_records(ShardIterator=shard_iterator, Limit=1)

        records = response["Records"]
        if records:
            record_data = records[0]["Data"]
            payload = json.loads(record_data.decode("utf-8"))

            img_base64, kinesis_name, geolocation = payload["image_data"], payload["origin"], payload["location"]
            img_bytes = base64.b64decode(img_base64)

            image = Image.open(io.BytesIO(img_bytes))

            labels, locations, scores = model(image)

            d_img = image
            for i in range(len(locations)):
                locations[i][0], locations[i][1], locations[i][2], locations[i][3] = int(locations[i][0]), int(locations[i][1]), int(locations[i][2]), int(locations[i][3])
                d_img = draw(d_img, locations[i], scores[i], labels[i])

            if 'accident' in labels:
                cv2.imwrite(f"../.temp/{counter}.jpg",d_img)
                s3.upload_file(Filename=f".temp/{counter}.jpg", Bucket=os.getenv("BUCKET_ID"), Key=f'Accident/{counter}.jpg')
                if timerStatus == False:
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        data = {"location": geolocation, "accident_code": "01212XYXY"}
                        response = await client.post(url, json=data)
                        
                        print(response.text)
                    asyncio.create_task(timer())
                try:
                    os.remove(f"../.temp/{counter}.jpg")
                except FileNotFoundError:
                    pass
            
            send_plain_image(d_img, kinesis)

        shard_iterator = response["NextShardIterator"]