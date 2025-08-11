import cv2
import base64

def send_plain_image(cap, kinesis, stream_name):
    _, jpeg = cv2.imencode(".jpg", cap)
    encoded = base64.b64encode(jpeg.tobytes()).decode()

    kinesis.put_record(
        StreamName=f"{stream_name}_inferenced",
        Data=encoded,
        PartitionKey="camera2"
    )