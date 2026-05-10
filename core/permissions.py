"""
Permissions for the API.
"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission to check if the user is the owner of an object.
    """
    
    def has_object_permission(self, request, view, obj):
        """Check if the user is the owner of the object."""
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'habit') and hasattr(obj.habit, 'user'):
            return obj.habit.user == request.user
        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Permission to check if the user is authenticated.
    """
    
    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user and request.user.is_authenticated
