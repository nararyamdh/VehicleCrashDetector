from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login
import sys
import json
import base64
import os
sys.path.append('../.')
from signup.models import WebAuthnCredential, WebAuthnCredential_UsersRecorded, UsersRecorded

@csrf_exempt
def begin_login(request):
    import json
    body = json.loads(request.body)

    try:
        global user
        user = User.objects.get(username=request.session['email'])
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found")

    email = user.username
    
    creds = WebAuthnCredential.objects.filter(user=user)

    allow_credentials = [
        {
            "type": "public-key",
            "id": base64.urlsafe_b64encode(cred.credential_id.encode()).decode().rstrip('=')
        } for cred in creds
    ]

    challenge = os.urandom(32)
    encoded_challenge = base64.urlsafe_b64encode(challenge).decode().rstrip('=')
    request.session['challenge'] = encoded_challenge
    request.session['user_id'] = user.id

    options = {
        "challenge": encoded_challenge,
        "timeout": 60000,
        "rpId": "ccd.ip-ddns.com",
        "allowCredentials": allow_credentials,
        "userVerification": "preferred"
    }

    return JsonResponse(options)

@csrf_exempt
def finish_login(request):
    if not request.session.get("challenge") or not request.session.get("user_id"):
        return HttpResponseBadRequest("Invalid session")

    challenge = request.session['challenge']
    user_id = request.session['user_id']

    data = json.loads(request.body)
    credential = data.get('credential')

    try:
        user = User.objects.get(id=user_id)
        login(request, user)
        return HttpResponse("Login successful.")
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found")

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email != '' and password != '':
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                request.session['login'] = True
                if 'email' in  request.session:
                    del request.session['email']
                request.session['email'] = email
                if WebAuthnCredential_UsersRecorded.objects.filter(email=email):
                    return redirect('mfa')
                else:
                    return redirect('mfa_su')
            else:
                return render(request, "login/login.html", {'error':"Either email or password is incorrect. Double-check email and password that you entered."})
        else:
            return render(request, "login/login.html", {'error':"Ensure that all of these filled correctly. All of these are important to fill and cannot leave these as blank."})
    return render(request, "login/login.html")

def MFA(request):
    return render(request, "MFA/MFA.html")