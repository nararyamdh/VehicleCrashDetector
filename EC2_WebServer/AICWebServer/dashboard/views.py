from django.shortcuts import render
from .models import Cameras, DataStream, History
import sys
import boto3
import requests
sys.path.append("../")
from signup.models import UsersRecorded
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def dashboard(request):
    items = Cameras.objects.all()
    if request.method == "POST":
        form_1(request)
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
            url = "https://bgr3ui8mpg.execute-api.ap-southeast-1.amazonaws.com/tel"
            data = {"location": "Jalan Diponegoro Nomor 48, Citarum, Kecamatan Bandung Wetan, Kota Bandung, Jawa Barat 40115","accident_code": "0AHU57AGSH"}

            response = requests.post(url, json=data)
            print(response)
            History.objects.create(call_from="+18567228212",call_to="+6285180802700")

    return render(request,"sos/sos.html",{"items_cam": items_cam, "items_oc": items_oc})

@csrf_exempt
def ds(request):
    items_kinesis = DataStream.objects.all()
    if request.method == "POST":
        form_1(request)

    return render(request,"ds/ds.html",{"items_kinesis": items_kinesis})

def form_1(request):
    if 'cctv_submit' in request.POST:
        cctv_get = request.POST.get('cctv_name')
        stream_name = request.POST.get('kinesis_name_1')

        if DataStream.objects.filter(camera_name=stream_name).exists():
            if not Cameras.objects.filter(camera_name=cctv_get).exists():
                Cameras.objects.create(camera_name=cctv_get,kinesis_datastream_name=stream_name)

    elif 'kinesis_submit' in request.POST:
        kinesis_client = boto3.client('kinesis', region_name='ap-southeast-1')
        stream_name = request.POST.get('kinesis_name_2')

        response = kinesis_client.create_stream(
            StreamName=stream_name,
            ShardCount=1
        )

        response2 = kinesis_client.create_stream(
            StreamName=f"{stream_name}_inference",
            ShardCount=1
        )

        DataStream.objects.create(camera_name=stream_name)