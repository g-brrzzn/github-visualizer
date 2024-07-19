from django.db import models
from django.contrib.auth.models import User

class GitHubProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    github_username = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.github_username

class Repository(models.Model):
    profile = models.ForeignKey(GitHubProfile, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
