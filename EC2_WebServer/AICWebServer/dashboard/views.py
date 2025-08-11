from django.shortcuts import render
from .models import Cameras, DataStream, History
import sys
import os
import boto3
import requests
sys.path.append("../")
from signup.models import UsersRecorded
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
def dashboard(request):
    items = Cameras.objects.all()
    return render(request,"dashboard/dashboard.html",{"items": items})

def iam(request):
    items = UsersRecorded.objects.all()
    items_cam = Cameras.objects.all()
    return render(request,"iam/iam.html",{"items": items, "items_cam": items_cam})

@csrf_exempt
def sos(request):
    items_cam = Cameras.objects.all()
    items_oc = History.objects.all()
    if request.method == "POST":
        if 'submit_3' in request.POST:
            url = os.getenv("TEL_TWILIO_API")
            data = {"location": "","accident_code": "0AHU57AGSH"}

            response = requests.post(url, json=data)
            print(response)
            History.objects.create(call_from=os.getenv("TEL_TWILIO_NUM"),call_to=os.getenv("TEL_TWILIO_DEST"))

    return render(request,"sos/sos.html",{"items_cam": items_cam, "items_oc": items_oc})

@csrf_exempt
def ds(request):
    items_kinesis = DataStream.objects.all()
    if request.method == "POST":
        if 'cctv_submit' in request.POST:
            pass
        elif 'kinesis_submit' in request.POST:
            kinesis_client = boto3.client('kinesis', region_name='ap-southeast-1')
            stream_name = request.POST.get('kinesis_name_2')

            response = kinesis_client.create_stream(
                StreamName=stream_name,
                ShardCount=3
            )

            DataStream.objects.create(camera_name=stream_name)

    return render(request,"ds/ds.html",{"items_kinesis": items_kinesis})