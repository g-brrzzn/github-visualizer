import requests
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import GitHubProfile, Repository
from .serializers import GitHubProfileSerializer, RepositorySerializer

class GitHubProfileViewSet(viewsets.ModelViewSet):
    queryset = GitHubProfile.objects.all()
    serializer_class = GitHubProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        github_username = request.data.get('github_username')
        additional_info = request.data.get('additional_info', '')

        profile_response = requests.get(f'https://api.github.com/users/{github_username}')
        if profile_response.status_code != 200:
            return Response({'error': 'GitHub user not found'}, status=status.HTTP_404_NOT_FOUND)
        profile_data = profile_response.json()

        user = request.user if request.user.is_authenticated else None
        profile, created = GitHubProfile.objects.get_or_create(
            github_username=github_username,
            defaults={
                'user': user,
                'bio': profile_data.get('bio', ''),
                'avatar_url': profile_data.get('avatar_url', ''),
                'additional_info': additional_info,
            }
        )
        
        if not created:
            profile.bio = profile_data.get('bio', '')
            profile.avatar_url = profile_data.get('avatar_url', '')
            profile.additional_info = additional_info
            profile.save()

        repos_response = requests.get(f'https://api.github.com/users/{github_username}/repos')
        repos_data = repos_response.json()
        for repo_data in repos_data:
            Repository.objects.get_or_create(
                profile=profile,
                name=repo_data['name'],
                defaults={
                    'description': repo_data['description'],
                    'url': repo_data['html_url'],
                }
            )

        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        profile = self.get_object()
        repo_name = request.data.get('name')
        try:
            repo = Repository.objects.get(profile=profile, name=repo_name)
            repo.is_favorite = not repo.is_favorite
            repo.save()
            return Response({'status': 'favorite status updated'})
        except Repository.DoesNotExist:
            return Response({'error': 'Repository not found'}, status=status.HTTP_404_NOT_FOUND)

def index(request):
    return render(request, 'api/index.html')
