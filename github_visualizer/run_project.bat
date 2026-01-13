@echo off
echo Initializing the Backend Django...
start cmd /k "cd github_visualizer && venv\Scripts\activate && python manage.py runserver"

echo Initializing the Frontend React...
start cmd /k "cd github_visualizer\frontend && npm start"

echo Project Initialized!