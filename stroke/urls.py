from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.ReactAppView.as_view()),
    #path('', views.create, name = 'main'),              #여기서 부터
    #path('show_train_result/', views.show_train_result, name='show_train_result'),
    #path('show_result/', views.show_result, name='show_result')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
