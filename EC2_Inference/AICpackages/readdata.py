import boto3
from dotenv import load_dotenv
import cv2
import numpy as np
import sys
sys.path.append("/home/ubuntu/AIC_Inference/processor")
from inference import Detector
sys.path.append("/home/ubuntu/AIC_Inference/AICpackages")
from draw import draw
from sender import send_plain_image
import asyncio
import httpx
import io
import os
import base64
import json
import time
sys.path.append("./")
from db import Database_X
from PIL import Image
from celery import Celery
from botocore.config import Config
from celery.utils.log import get_task_logger

load_dotenv("../.credentials")

app = Celery('DL_kinesis_tasks', broker='redis://localhost:6379/0')

logger = get_task_logger(__name__)

url = "https://bgr3ui8mpg.execute-api.ap-southeast-1.amazonaws.com/tel"

timerStatus = False

config = Config(
            max_pool_connections=50,
            retries={'max_attempts': 3}
        )

async def timer():
    global timerStatus
    print("Timer running...")
    timerStatus = True
    await asyncio.sleep(60*30)
    timerStatus = False


async def readdatah(stream_name):
    relation = Database_X()
    kinesis = boto3.client("kinesis", 
                            aws_access_key_id=os.getenv("ACCESS_KEY"),
                            aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                            region_name="ap-southeast-1",
                            config=config)
    s3 = boto3.client("s3", 
                      region_name="ap-southeast-1")
    
    active_shards = []
    stream_description = kinesis.describe_stream(StreamName=stream_name)
    for shard in stream_description["StreamDescription"]["Shards"]:
        seq_range = shard["SequenceNumberRange"]
        if "EndingSequenceNumber" not in seq_range:
            active_shards.append(shard["ShardId"])

    if not active_shards:
        raise Exception("Tidak ada shard aktif")

    shard_id = active_shards[0]
    shard_iterator = kinesis.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType="LATEST"
    )["ShardIterator"]

    model = Detector()

    logger.info("Initialized...")

    counter = 0
    while True:
        response = kinesis.get_records(ShardIterator=shard_iterator, Limit=1)
    
        records = response["Records"]
    
        logger.info("Gaining data... ")

        records = response["Records"]
        if records:
            logger.info("Got data. ")
            record_data = records[0]["Data"]
            payload = json.loads(record_data.decode("utf-8"))

            img_base64, kinesis_name, geolocation, timestamp = payload["image_data"], payload["origin"], payload["location"], payload["time_stamp"]
            img_bytes = base64.b64decode(img_base64)

            image = Image.open(io.BytesIO(img_bytes))

            labels, locations, scores = model.detect(image)

            d_img = np.array(image)
            for i in range(len(locations)):
                locations[i][0], locations[i][1], locations[i][2], locations[i][3] = int(locations[i][0]), int(locations[i][1]), int(locations[i][2]), int(locations[i][3])
                d_img = draw(d_img, locations[i], scores[i], labels[i])

            if 'vehicle' in labels:
                relation.vech_update(kinesis_name)

            if 'accident' in labels:
                logger.info("Accident detected...")
                relation.acc_update(kinesis_name)
                cv2.imwrite(f"/home/ubuntu/AIC_Inference/.temp/{stream_name}_{counter}.jpg",d_img)
                s3.upload_file(Filename=f"/home/ubuntu/AIC_Inference/.temp/{stream_name}_{counter}.jpg", Bucket='app-bucket-8283', Key=f'Accident/{counter}.jpg')

                if timerStatus == False:
                    print("API running...")
                    relation.tel_update(kinesis_name)
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        data = {"location": geolocation, "accident_code": "01212XYXY"}
                        response = await client.post(url, json=data)
                        print(response.text)
                    asyncio.create_task(timer())
                try:
                    os.remove(f"/home/ubuntu/AIC_Inference/.temp/{counter}.jpg")
                except FileNotFoundError:
                    pass
                counter+=1
            send_plain_image(d_img, kinesis, stream_name)

        records_response = kinesis.get_records(ShardIterator=shard_iterator, Limit=10)
        shard_iterator = records_response["NextShardIterator"]
        time.sleep(1)

@app.task()
def run(stream_name):
    asyncio.run(readdatah(stream_name))