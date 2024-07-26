import requests
from rest_framework.views import APIView
from rest_framework.response import Response

class UserProfileView(APIView):
    def get(self, request, username):
        profile_response = requests.get(f'https://api.github.com/users/{username}')
        if profile_response.status_code != 200:
            return Response({'error': 'GitHub user not found'}, status=404)
        profile_data = profile_response.json()

        repos_response = requests.get(f'https://api.github.com/users/{username}/repos')
        if repos_response.status_code != 200:
            return Response({'error': 'GitHub repos not found'}, status=404)
        repos_data = repos_response.json()

        repos_data = [repo for repo in repos_data if repo['name'] != username]

        def calculate_repo_score(repo):
            return (repo['stargazers_count'] * 0.5) + (repo['watchers_count'] * 0.3) + (repo['forks_count'] * 0.2)
        
        repos_data.sort(key=lambda repo: (calculate_repo_score(repo), repo['size']), reverse=True)

        response_data = {
            'profile': {
                'bio': profile_data.get('bio', ''),
                'avatar_url': profile_data.get('avatar_url', ''),
                'name': profile_data.get('name', ''),
                'login': profile_data.get('login', ''),
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
                    'stargazers_count': repo['stargazers_count'],
                    'watchers_count': repo['watchers_count'],
                    'forks_count': repo['forks_count']
                }
                for repo in repos_data
            ]
        }

        return Response(response_data)
