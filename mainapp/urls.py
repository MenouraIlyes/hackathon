from django.urls import path
from .views import create_user, get_users

urlpatterns = [
    path("create_user/", create_user, name="create_user"),
    path("get_users/", get_users, name="get_users"),
]
