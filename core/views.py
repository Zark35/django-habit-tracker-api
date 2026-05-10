"""
Core views for the API.
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class APIRootView(APIView):
    """
    API Root - Welcome endpoint that provides links to available resources.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Return available API endpoints.
        """
        return Response({
            'message': 'Welcome to Habit Tracker API',
            'version': '1.0.0-alpha',
            'endpoints': {
                'documentation': {
                    'swagger': request.build_absolute_uri('/api/docs/'),
                    'redoc': request.build_absolute_uri('/api/redoc/'),
                    'schema': request.build_absolute_uri('/api/schema/'),
                },
                'authentication': {
                    'register': request.build_absolute_uri('/api/auth/register/'),
                    'login': request.build_absolute_uri('/api/auth/token/'),
                    'refresh': request.build_absolute_uri('/api/auth/token/refresh/'),
                },
                'habits': {
                    'list': request.build_absolute_uri('/api/habits/'),
                },
                'tracking': {
                    'entries': request.build_absolute_uri('/api/tracking/entries/'),
                },
            }
        })
