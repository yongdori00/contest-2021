from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.ReactAppView.as_view()),
<<<<<<< HEAD
    #path('', views.create, name = 'main'),              #여기서 부터
    #path('show_train_result/', views.show_train_result, name='show_train_result'),
    #path('show_result/', views.show_result, name='show_result')
=======
    #path('', views.create, name = 'main'),
    #path('submit_photo/', views.SubmitPhotoView.as_view()),                #여기서 부터
    path('show_train_result/', views.show_train_result, name='show_train_result'),
    path('show_result/', views.show_result, name='show_result')
>>>>>>> refs/remotes/origin/main
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
