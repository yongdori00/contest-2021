from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from .forms import UploadImageForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .train import training
from .results import result_main

def create(request):
    return render(request, 'stroke/main.html', {})

def get_image(request):
    # 글을 쓸때는 여기 수행
    # 글쓰기를 눌렀을땐 여기로
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)  # 이미지르 업로드할때 쓰는 form
        # form을 받아서 그게 유요한지 테스트 후 
        if form.is_valid():
            myfile = request.FILES['image']
            # 
            fs = FileSystemStorage()  # 이미지 파일을 저장할때 쓰는 함수
            filename = fs.save(myfile.name, myfile)
            # 이미지를 업로드 하고
            uploaded_file_url = fs.url(filename)
            # html로 렌더링
            return render(request, 'stroke/uimage.html', {'form': form, 'uploaded_file_url' : uploaded_file_url})
    # 보여줄 때는 이곳 수행
    # 제일 처음엔 form을 받아와서 uimage.html에 보내주고
    else:
        form = UploadImageForm()
        return render(request, 'stroke/uimage.html', {'form': form})
        
def show_train_result(request):
    result_str = ''
    if request.method =='POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name
            
            result_str = training(settings.MEDIA_ROOT_URL + imageURL)

            return render(request, 'stroke/show_train_result.html',{'form':form,'post':post, 'result_str':result_str})
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

