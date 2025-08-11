import json
import sys
from dotenv import load_dotenv
sys.path.append(".")
import os
from twilio.rest import Client

load_dotenv(".credentials")

def lambda_handler(event, context):
    # TODO implement
    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    body = json.loads(event.get('body', '{}'))

    location = body.get('location', 'Tidak diketahui')
    accident_code = body.get('accident_code', '0X0X0X0X')

    response = f'<Response><Say language="id-ID" voice="Google.id-ID-Chirp3-HD-Fenrir">Peringatan! Pesan ini hanya dibacakan sekali dan tidak akan diulangi.</Say><Pause length="2" /><Say language="id-ID" voice="Google.id-ID-Chirp3-HD-Fenrir">Mohon bantuannya sekarang! terjadi kecelakaan yang berada di lokasi {location}. Saya berharap bantuan datang sekarang. Saya atas nama asisten AI pemantau kecelakaan di jalan raya mengucapkan terima kasih atas bantuan anda. Kode kecelakaan {accident_code}</Say></Response>'

    call = client.calls.create(
        twiml=response,
        to=os.getenv("CALL_TO"),
        from_=os.getenv("CALL_FROM"),
    )

    return {
        'statusCode': 200,
        'body': call.sid
    }
