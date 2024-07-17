from rest_framework import serializers
from .models import GitHubProfile, Repository

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'

class GitHubProfileSerializer(serializers.ModelSerializer):
    repositories = RepositorySerializer(many=True, read_only=True)

    class Meta:
        model = GitHubProfile
        fields = '__all__'
