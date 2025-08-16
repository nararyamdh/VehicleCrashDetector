import cv2
import base64

def send_plain_image(cap, kinesis, stream_name):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    _, jpeg = cv2.imencode(".jpg", cap, encode_param)
    encoded = base64.b64encode(jpeg.tobytes()).decode("utf-8")

    kinesis.put_record(
        StreamName=f"{stream_name}_inference",
        Data=encoded,
        PartitionKey="camera"
    )