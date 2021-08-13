from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from .forms import UploadImageForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .train import training
from .results import result_main
import os
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from .models import ImageUploadModel
from .serializers import ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import viewsets
import base64
import json

class ReactAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(str(settings.BASE_DIR),
                                    'frontend',
                                    'build',
                                    'index.html')) as file:
                return HttpResponse(file.read())

        except:
            
            return HttpResponse(status=501,)
        
    def post(self, request):
        data = json.loads(request.body)
        ide = data['description']
        doc = data['document']

        new_doc = doc[23:]

        ide = settings.MEDIA_ROOT_URL + settings.MEDIA_URL + ide + "_new.jpg"

        result_str, cropped_img = result_main(new_doc, True, ide)
        context = {'result':result_str, 'image':cropped_img}

        return JsonResponse(context, safe=False)
        

'''
def create(request):
    return render(request, 'stroke/main.html', {})
'''

class SubmitPhotoView(viewsets.ModelViewSet):
    queryset = ImageUploadModel.objects.all()
    serializer_class = ImageUploadSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

'''def show_train_result(request):
    result_str = ''
    if request.method =='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name
            
            training(settings.MEDIA_ROOT_URL + imageURL)

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
            
            result_str = result_main(settings.MEDIA_ROOT_URL + imageURL, is_capture = False)

            get_image_url = imageURL         #output 이미지
            temp_get_image_url = get_image_url[:-4]
            temp_get_image_url = temp_get_image_url + '_new.jpg'

            return render(request, 'stroke/show_result.html',{'form':form,'post':post,'result_str':result_str, 'get_image' : temp_get_image_url})
    else:
        form = ImageUploadForm()
    return render(request, 'stroke/show_result.html',{'form':form})'''
