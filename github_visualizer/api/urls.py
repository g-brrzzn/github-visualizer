from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import GitHubProfileViewSet
from django.urls import path
from .views import index
from .auth import CustomAuthToken

router = routers.DefaultRouter()
router.register(r'profiles', GitHubProfileViewSet, basename='github-profile')

urlpatterns = [
    path('profiles/', GitHubProfileViewSet.as_view({'post': 'create'}), name='create-profile'),
    path('profiles/<int:pk>/favorite/', GitHubProfileViewSet.as_view({'post': 'favorite'}), name='favorite-repo'),
    path('index/', index, name='index'),
    path('token/', CustomAuthToken.as_view(), name='get-token'),
    path('', include(router.urls)),
    path('', index, name='index'),
]
