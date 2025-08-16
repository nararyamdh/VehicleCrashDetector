import boto3
import os
import cv2
import sys
sys.path.append(os.path.abspath("/Volumes/AryaMD/Me/Project/AIC_Micro/connector"))
from camera import Camera
import time
from celery import shared_task

def available_camera():
    available_cams = []

    count = 0
    while True:
        cam = cv2.VideoCapture(count)
        available_cams.append(count)
        if not cam.isOpened():
            break
        count+=1
    
    return min(available_cams), max(available_cams)

@shared_task
def start_camera(id, stream_name, partkey, location):
    live = Camera(int(id), stream_name, partkey, location)

    try:
        while True:
            live.camera()
            time.sleep(0.05) 
    except KeyboardInterrupt:
        pass
    finally:
        live.video.release()
        cv2.destroyAllWindows()
        live.pool.shutdown()