import base64
import asyncio
import boto3
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv
import os
import json

from django.urls import re_path

load_dotenv("../../.credentials")

kinesis = boto3.client("kinesis", 
                        aws_access_key_id=os.getenv("ACCESS_KEY"),
                        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                        region_name="ap-southeast-1")

class ImageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_running = True
        streams_get = kinesis.list_streams()["StreamNames"]
        # self.stream_name = self.scope["url_route"]["kwargs"]["stream_name"]

        streams_processing = []
        self.stream_name = "test59"
        info = kinesis.describe_stream_summary(StreamName=self.stream_name)
        status = info["StreamDescriptionSummary"]["StreamStatus"]
        # if status == "ACTIVE" and not '_inference' in self.stream_name and self.stream_name not in streams_processing:
        #     print(">>> CONNECT 1", self.scope["path"])
        #     await self.channel_layer.group_add(self.stream_name, self.channel_name)
        #     print(">>> CONNECT 2*", self.scope["path"])
        #     await self.accept()

        asyncio.create_task(self.stream_images(self.stream_name))

    async def disconnect(self, close_code):
        self.keep_running = False

    async def stream_images(self, stream_name):
        print("Finish 1")
        active_shards = []
        stream_description = kinesis.describe_stream(StreamName=stream_name)
        for shard in stream_description["StreamDescription"]["Shards"]:
            seq_range = shard["SequenceNumberRange"]
            if "EndingSequenceNumber" not in seq_range:
                active_shards.append(shard["ShardId"])

        if not active_shards:
            raise Exception("Tidak ada shard aktif")

        shard_id = active_shards[0]
        print("Finish 2")

        shard_iterator = kinesis.get_shard_iterator(
            StreamName=stream_name+"_inference",
            ShardId=shard_id,
            ShardIteratorType="LATEST"
        )["ShardIterator"]

        while self.keep_running:
            resp = kinesis.get_records(ShardIterator=shard_iterator, Limit=1)
            shard_iterator = resp["NextShardIterator"]
            print("Finish 3")

            if resp["Records"]:
                data_raw = resp["Records"][0]["Data"]

                payload = data_raw.decode("utf-8")
                print("Finish 4")

                await self.send(payload)

            await asyncio.sleep(1)
