from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
import random, string
import openpyxl
from .models import Student
from .manager import generate_qr
import json
from imagekitio import ImageKit
import os

# def home(request):
#     return redirect('/login')

@csrf_exempt
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            registration_id = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=registration_id, password=password)
            if user is not None:
                login(request, user=user)
                request.session['user'] = registration_id
                return redirect('/')
            else:
                messages.error(request, 'Invalid password or account not activated')
                return redirect("/login")
        else:
            return render(request=request, template_name='login.html')
    else:
        return redirect('/events')


def logout_user(request):
    logout(request)
    return redirect('/login')


def upload_qr(file_path, secure_id):
    imagekit = ImageKit(
    public_key= os.getenv('IMAGEKIT_PUBLIC_KEY', None),
    private_key=os.getenv('IMAGEKIT_PRIVATE_KEY', None),
    url_endpoint = os.getenv('IMAGEKIT_URL_ENDPOINT', None),
    )
    upload = imagekit.upload(
    file=open(file_path, "rb"),
    file_name= file_path
    )
    image_url = upload.response_metadata.raw['url']
    os.remove(file_path)
    return image_url

