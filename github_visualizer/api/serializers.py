from rest_framework import serializers
from .models import GitHubProfile, Repository, Profile

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'

class GitHubProfileSerializer(serializers.ModelSerializer):
    repositories = RepositorySerializer(many=True, read_only=True)

    class Meta:
        model = GitHubProfile
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'bio']

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['name', 'description', 'stargazers_count', 'forks_count']