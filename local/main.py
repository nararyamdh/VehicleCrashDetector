import boto3
import os
import cv2
import base64
from AICpackages.sender import read_camera_plain, send_unplain_image
from AICpackages.receiver import Detector
from AICpackages.draw import draw
from PIL import Image
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

cap = cv2.VideoCapture(1)
kinesis = boto3.client("kinesis", region_name="ap-southeast-1")
s3 = boto3.client('s3',region_name='ap-southeast-1')
detection = Detector()
url = os.getenv("API_URL")
data = {"key1": "", "key2": ""}

width, height = cap.get(3), cap.get(4)

global counter, timerStatus
counter, timerStatus = 0, False

async def timer():
    global timerStatus
    print("Timer berjalan...")
    timerStatus = True
    await asyncio.sleep(60*30)
    timerStatus = False

async def main():
    global counter, timerStatus
    while True:
        img = read_camera_plain(cap, kinesis)
        img_pil = Image.fromarray(img)
        
        labels, locations, score = detection.detect(img_pil)

        print(labels, locations, score)

        d_img = img
        for i in range(len(locations)):
            locations[i][0], locations[i][1], locations[i][2], locations[i][3] = int(locations[i][0]), int(locations[i][1]), int(locations[i][2]), int(locations[i][3])
            d_img = draw(d_img, locations[i], score[i], labels[i])

        if 'accident' in labels:
            cv2.imwrite(f".temp/{counter}.jpg",d_img)
            s3.upload_file(Filename=f".temp/{counter}.jpg", Bucket='app-bucket-8283', Key=f'Accident/{counter}.jpg')
            if timerStatus == False:
                async with httpx.AsyncClient(timeout=60.0) as client:

                    response = await client.post(url, json=data)
                    print(response.text)
                asyncio.create_task(timer())
            try:
                os.remove(f".temp/{counter}.jpg")
            except FileNotFoundError:
                pass
        
        send_unplain_image(d_img, kinesis)

        cv2.imshow("Capture", d_img)

        if cv2.waitKey(1) == ord('q'):
            break

        counter+=1

    cap.release()
    cv2.destroyAllWindows()

asyncio.run(main())