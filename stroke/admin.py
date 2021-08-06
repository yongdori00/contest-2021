from django.contrib import admin
from .models import ImageUploadModel

# Photo 클래스를 inline으로 나타낸다.

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다. 
# Register your models here.

admin.site.register(ImageUploadModel)