from django.shortcuts import render, redirect
from signup.models import WebAuthnCredential, UsersRecorded, AccessKey, WebAuthnCredential_UsersRecorded
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import sys
import os
import base64
os.environ["LD_LIBRARY_PATH"] = "/usr/lib/x86_64-linux-gnu"
sys.path.append('../.')
from django.http import JsonResponse, HttpResponse
import json

from django.contrib.auth.models import User
# 
# from webauthn import (
#     base64url_to_bytes,
# )
# from webauthn.helpers import (
#     bytes_to_base64url
# )
# from webauthn.helpers.cose import COSEAlgorithmIdentifier
# from webauthn.helpers.structs import (
#     AttestationConveyancePreference,
#     AuthenticatorAttachment,
#     AuthenticatorSelectionCriteria,
#     PublicKeyCredentialDescriptor,
#     PublicKeyCredentialHint,
#     ResidentKeyRequirement,
#     PublicKeyCredentialCreationOptions, 
#     UserVerificationRequirement
# )
# from django.contrib.auth.models import User
# from signup.models import Users_Data


# def begin_register(request):
#     user = request.user
#     options = generate_registration_options(
#         rp_id='ccd.ip-ddns.com',
#         rp_name='VCD Credential',
#         user_id=str(user.id),
#         user_name=user.username,
#     )
#     request.session['challenge'] = options.challenge
#     return JsonResponse(options.model_dump())

# def finish_register(request):
#     body = json.loads(request.body)
#     try:
#         result = verify_registration_response(
#             credential=body,
#             expected_challenge=request.session['challenge'],
#             expected_origin='https://ccd.ip-ddns.com',
#             expected_rp_id='ccd.ip-ddns.com',
#         )
#         WebAuthnCredential.objects.create(
#             user=request.user,
#             credential_id=result.credential_id,
#             public_key=result.credential_public_key,
#             sign_count=result.sign_count,
#             rp_id='ccd.ip-ddns.com'
#         )
#         return JsonResponse({'status': 'ok'})
#     except InvalidRegistrationResponse as e:
#         return JsonResponse({'status': 'error', 'reason': str(e)}, status=400)


def b64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def begin_register(request):
    user = request.user

    challenge = os.urandom(32)
    request.session['challenge'] = b64url_encode(challenge)

    options = {
        "challenge": b64url_encode(challenge),
        "rp": {
            "name": "VCD App",
            "id": "ccd.ip-ddns.com"
        },
        "user": {
            "id": b64url_encode(str(user.id).encode()),
            "name": user.username,
            "displayName": user.username
        },
        "pubKeyCredParams": [
            {"type": "public-key", "alg": -7},    # ES256
            {"type": "public-key", "alg": -257},  # RS256
        ],
        "timeout": 60000,
        "attestation": "none"
    }

    return JsonResponse(options)


@csrf_exempt
def finish_register(request):
    data = json.loads(request.body)
    credential = data['credential']
    user = request.user

    WebAuthnCredential.objects.create(
        user=user,
        credential_id=credential['id'],
        public_key=credential['response']['attestationObject'],
        sign_count=0
    )

    WebAuthnCredential_UsersRecorded.objects.create(
        id_user=user.id,
        email=user.username
    )

    return HttpResponse("Registered.")

@csrf_exempt
def signup(request):
    if 'signup' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password_1 = request.POST.get('password')
            password_2 = request.POST.get('password2')
            if name != '' and email != '' and password_1 != '' and password_2 != '' and password_1 == password_2:
                if not UsersRecorded.objects.filter(email=email) and not User.objects.filter(username=email):
                    User.objects.create_user(username=email, password=password_1)
                   
                    request.session['name'] = name
                    request.session['email'] = email
                    request.session['password'] = password_1

                    UsersRecorded.objects.create(name=name,email=email)

                    request.session['id'] = UsersRecorded.objects.filter(email=email).values_list('id_x', flat=True).first()

                    return redirect('login')
                else:
                    return render(request, "signup/signup.html",{'error':"Someone already have this account. You must enter another email."})
            else:
                return render(request, "signup/signup.html",{'error':"Ensure that all of these filled correctly. All of these are important to fill and cannot leave these as blank."})
        return render(request, "signup/signup.html")
    else:
        return redirect('permission')

def MFA_su(request):
    return render(request, "MFA/MFA_su.html")

@csrf_exempt
def permission(request):
    if 'signup' not in request.session:
        if request.method == 'POST':
            acc1 = request.POST.get('acc1')
            acc2 = request.POST.get('acc2')
            if acc1 != '' and acc2 != '':
                data = AccessKey.objects.filter(access_key_1=acc1,access_key_2=acc2)
                if data:
                    request.session['signup'] = True
                    return redirect('signup')
                else:
                    return render(request, "permission/permission.html",{'error':"Filled access key didn't match on any recorded access key in our database. please contact your administrator to gain more informations."})
            else:
                return render(request, "permission/permission.html",{'error':"Ensure that all of these filled correctly. All of these are important to fill and cannot leave these as blank."})
        return render(request, "permission/permission.html")
    else:
        return redirect('signup')