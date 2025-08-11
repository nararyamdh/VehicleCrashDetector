import cv2
import base64

def read_camera_plain(cap, kinesis):
    _, frame = cap.read()

    _, jpeg = cv2.imencode(".jpg", frame)
    encoded = base64.b64encode(jpeg.tobytes()).decode()

    kinesis.put_record(
        StreamName="kinesis_plain",
        Data=encoded,
        PartitionKey="camera1"
    )

    return frame

def send_unplain_image(cap, kinesis):
    _, jpeg = cv2.imencode(".jpg", cap)
    encoded = base64.b64encode(jpeg.tobytes()).decode()

    kinesis.put_record(
        StreamName="kinesis_unplain",
        Data=encoded,
        PartitionKey="camera2"
    )