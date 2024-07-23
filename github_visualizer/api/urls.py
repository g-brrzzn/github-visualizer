from django.urls import path, include
from rest_framework import routers
from .views import UserProfileView, index

urlpatterns = [
    path('api/profiles/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('index/', index, name='index'),
]
