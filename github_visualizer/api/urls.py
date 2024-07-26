from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('api/profiles/<str:username>/', UserProfileView.as_view(), name='user-profile'),
]
