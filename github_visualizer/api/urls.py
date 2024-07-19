from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import GitHubProfileViewSet
from django.urls import path
from .views import index, UserProfileView


router = routers.DefaultRouter()
router.register(r'profiles', GitHubProfileViewSet, basename='github-profile')

urlpatterns = [
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('index/', index, name='index'),
    path('api/', include(router.urls)),
    path('', include(router.urls)),
    path('', index, name='index'),
]
