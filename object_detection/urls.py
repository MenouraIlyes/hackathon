from django.urls import path
from .views import detect_people
from .views import detect_people_video

urlpatterns = [
    path('detect/', detect_people, name='detect_people'),
    path('detect-video/', detect_people_video, name='detect_people_video'),
]
