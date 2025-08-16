from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import sys
import os
sys.path.append(os.path.abspath("/Volumes/AryaMD/Me/Project/AIC_Micro/"))
from connector.main import start_camera, available_camera
from connector.checker import  check_active

id, kinesis, location = "", "", ""

@csrf_exempt
def setup(request):
    min_x, max_x = available_camera()
    if request.method == 'POST':
        if 'submit_btn' in request.POST:
            global id, kinesis, location
            kinesis = request.POST.get('kinesis')
            location = request.POST.get('location')
            id = request.POST.get('camera')

            if not kinesis or not id:
                return redirect('failed')
            else:
                if check_active(kinesis) and (int(id) >= min_x and int(id) <= max_x):
                    return redirect('success')
                else:
                    return redirect('failed')
    return render(request, "kinesis_setup.html", {"min_x":min_x,"max_x":max_x})

def success(request):
    start_camera.delay(id, kinesis, "Key01", location)
    return render(request, "success.html")

def failed(request):
    return render(request, "failed.html")