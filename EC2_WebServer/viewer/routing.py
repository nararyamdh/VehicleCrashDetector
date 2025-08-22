from django.urls import re_path
from . import consumers

# import sys
# sys.path.append('../')
# from dashboard.models import Cameras
# from dotenv import load_dotenv
# import boto3
# import os

# load_dotenv("../../.credentials")

# kinesis = boto3.client("kinesis", 
#                         aws_access_key_id=os.getenv("ACCESS_KEY"),
#                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
#                         region_name="ap-southeast-1")

# streams_get = kinesis.list_streams()["StreamNames"]
# streams_processing = []

# for name in streams_get:
#     info = kinesis.describe_stream_summary(StreamName=name)
#     status = info["StreamDescriptionSummary"]["StreamStatus"]
#     if status == "ACTIVE" and not '_inference' in name and name not in streams_processing:
#         streams_processing.append(name)


websocket_urlpatterns = [
    # re_path(r"^ws/image/(?P<stream_name>[\w-]+)/$", consumers.ImageConsumer.as_asgi()),
    re_path(r"^ws/image/$", consumers.ImageConsumer.as_asgi()),
]