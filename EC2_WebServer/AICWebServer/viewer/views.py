from django.shortcuts import render
import boto3
import base64
from django.views import View

# class IframeKinesisPlain(View):
#     def get(self, request):
#         client = boto3.client('kinesis', region_name='ap-southeast-1')
#         stream_name = 'kinesis_plain'

#         shards = client.describe_stream(StreamName=stream_name)['StreamDescription']['Shards']
#         shard_id = shards[0]['ShardId']

#         shard_iterator = client.get_shard_iterator(
#             StreamName=stream_name,
#             ShardId=shard_id,
#             ShardIteratorType='LATEST'
#         )['ShardIterator']

#         records = client.get_records(ShardIterator=shard_iterator, Limit=1)['Records']
#         if not records:
#             return HttpResponse("NOTHING HERE", content_type="text/plain")

#         data_base64 = records[0]['Data']
#         image_bytes = base64.b64decode(data_base64)
        
#         return HttpResponse(image_bytes, content_type="image/jpeg")

def viewer(request):
    return render(request, "index/SingleViewer.html")

def captures(request):
    return render(request, "captures/Captures.html")

def recognized(request):
    return render(request, "recognized_people/Rec.html")

def alarm(request):
    return render(request, "alarm_monitor/Alarm.html")
