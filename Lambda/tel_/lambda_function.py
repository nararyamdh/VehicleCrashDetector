import json
import sys
sys.path.append(".")
from twilio.rest import Client

def lambda_handler(event, context):
    # TODO implement
    account_sid = "AC51e1549702874aad90c1ee5a843ee504"
    auth_token = "71b32cebe6d27608ff94670d9e4b82c5"
    client = Client(account_sid, auth_token)

    body = json.loads(event.get('body', '{}'))

    location = body.get('location', 'Tidak diketahui')
    accident_code = body.get('accident_code', '0X0X0X0X')

    response = f'<Response><Say language="id-ID" voice="Google.id-ID-Chirp3-HD-Fenrir">Peringatan! Pesan ini hanya dibacakan sekali dan tidak akan diulangi.</Say><Pause length="2" /><Say language="id-ID" voice="Google.id-ID-Chirp3-HD-Fenrir">Mohon bantuannya sekarang! terjadi kecelakaan yang berada di lokasi {location}. Saya berharap bantuan datang sekarang. Saya atas nama asisten AI pemantau kecelakaan di jalan raya mengucapkan terima kasih atas bantuan anda. Kode kecelakaan {accident_code}</Say></Response>'

    call = client.calls.create(
        twiml=response,
        to="+6281316435939",
        from_="+14408052681",
    )

    return {
        'statusCode': 200,
        'body': call.sid
    }
