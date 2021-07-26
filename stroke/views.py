from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from .forms import UploadImageForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .train import training
from .results import result_main
import os

def create(request):
    return render(request, 'stroke/main.html', {})

def show_train_result(request):
    result_str = ''
    if request.method =='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name
            
            result_str = training(settings.MEDIA_ROOT_URL + imageURL)

            get_image_url = imageURL         #output 이미지
            temp_get_image_url = get_image_url[:-4]
            temp_get_image_url = temp_get_image_url + '_new.jpg'

            return render(request, 'stroke/show_train_result.html',{'form':form,'post':post,'result_str':result_str, 'get_image' : temp_get_image_url})
    else:
        form = ImageUploadForm()
    return render(request, 'stroke/show_train_result.html',{'form':form})

def show_result(request):
    if request.method =='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name
            
            result_main(settings.MEDIA_ROOT_URL + imageURL, is_capture = False)

            return render(request, 'stroke/show_result.html',{'form':form,'post':post})
    else:
        form = ImageUploadForm()
    return render(request, 'stroke/show_result.html',{'form':form})

def capture(request):
    if request.method =='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name
            
            #result_main(settings.MEDIA_ROOT_URL + imageURL, is_capture = False)

            return render(request, 'stroke/capture.html',{'form':form,'post':post})
    else:
        form = ImageUploadForm()
    return render(request, 'stroke/capture.html',{'form':form})

