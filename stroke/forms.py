from django import forms
from .models import ImageUploadModel

# urls에서 요청이 오면 first_view로 오는데, 이 때 ~.html을 rendering 해줘라
class UploadImageForm(forms.Form):
    title = forms.CharField(max_length = 50)
    image = forms.ImageField()

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('description','document')