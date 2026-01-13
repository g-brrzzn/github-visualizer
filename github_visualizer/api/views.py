import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserProfileView(APIView):
    def get(self, request, username):
        github_token = os.getenv('GITHUB_TOKEN')
        headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if github_token:
            headers['Authorization'] = f'token {github_token}'
            
        timeout_seconds = 5

        try:
            profile_url = f'https://api.github.com/users/{username}'
            profile_response = requests.get(profile_url, headers=headers, timeout=timeout_seconds)
            
            if profile_response.status_code == 404:
                return Response({'error': 'GitHub user not found'}, status=status.HTTP_404_NOT_FOUND)
            elif profile_response.status_code != 200:
                return Response({'error': 'GitHub API error'}, status=profile_response.status_code)
            
            profile_data = profile_response.json()

            repos_url = f'https://api.github.com/users/{username}/repos?per_page=100'
            repos_response = requests.get(repos_url, headers=headers, timeout=timeout_seconds)
            
            if repos_response.status_code != 200:
                return Response({'error': 'Failed to fetch repositories'}, status=repos_response.status_code)
            
            repos_raw_data = repos_response.json()
            repos_filtered = [repo for repo in repos_raw_data if repo['name'].lower() != username.lower()]

            def calculate_repo_score(repo):
                return (repo.get('stargazers_count', 0) * 0.5) + \
                       (repo.get('watchers_count', 0) * 0.3) + \
                       (repo.get('forks_count', 0) * 0.2)
            
            repos_filtered.sort(
                key=lambda repo: (calculate_repo_score(repo), repo.get('size', 0)), 
                reverse=True
            )

            response_data = {
                'profile': {
                    'name': profile_data.get('name'),
                    'login': profile_data.get('login'),
                    'bio': profile_data.get('bio', ''),
                    'avatar_url': profile_data.get('avatar_url', ''),
                    'public_repos': profile_data.get('public_repos', 0),
                    'location': profile_data.get('location', ''),
                    'company': profile_data.get('company', ''),
                    'email': profile_data.get('email', ''),
                    'followers': profile_data.get('followers', 0),
                    'following': profile_data.get('following', 0)
                },
                'repositories': [
                    {
                        'name': repo['name'],
                        'description': repo.get('description', ''),
                        'url': repo['html_url'],
                        'stargazers_count': repo.get('stargazers_count', 0),
                        'watchers_count': repo.get('watchers_count', 0),
                        'forks_count': repo.get('forks_count', 0),
                        'language': repo.get('language', '')
                    }
                    for repo in repos_filtered
                ]
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except requests.exceptions.Timeout:
            return Response({'error': 'GitHub API request timed out'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Connection error: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)