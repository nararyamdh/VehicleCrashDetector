from django.shortcuts import render, get_object_or_404
import boto3
import base64
from django.views import View
import sys
sys.path.append('../')
from dashboard.models import Cameras
from dotenv import load_dotenv
from . import consumers
import os

load_dotenv("../../.credentials")

s3 = boto3.client("s3", 
                aws_access_key_id=os.getenv("ACCESS_KEY"),
                aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
                region_name="ap-southeast-1")

def viewer(request, id_x):
    cam = get_object_or_404(Cameras, pk=id_x)
    get_object = Cameras.objects.filter(id_x=id_x).values("id_x", "kinesis_datastream_name").first()
    stream_name = get_object["kinesis_datastream_name"]
    consumers.var = stream_name
    print(stream_name)
    return render(request, "index/SingleViewer.html",{"data_cam":cam, "stream_name":stream_name})

def captures(request, id_x):
    cam = get_object_or_404(Cameras, pk=id_x)
    response = s3.list_objects_v2(Bucket='app-bucket-8283')

    objects = []
    if 'Contents' in response:
        for obj in response['Contents']:
            url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': 'app-bucket-8283',
                    'Key': obj['Key']
                },
                ExpiresIn=3600
            )

            objects.append({
                'key': obj['Key'],
                'size': int(obj['Size'])*0.001,
                'last_modified': obj['LastModified'],
                'url': url
            })
    return render(request, "captures/Captures.html",{"data_cam":cam,'objects': objects})

def manual(request, id_x):
    cam = get_object_or_404(Cameras, pk=id_x)
    return render(request, "manual/manual.html",{"data_cam":cam})

def metrics(request, id_x):
    cam = get_object_or_404(Cameras, pk=id_x)
    return render(request, "metrics/Metrics.html",{"data_cam":cam})

def alarm(request, id_x):
    cam = get_object_or_404(Cameras, pk=id_x)
    return render(request, "alarm_monitor/Alarm.html",{"data_cam":cam})
