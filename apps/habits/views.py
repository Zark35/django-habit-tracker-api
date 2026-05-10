"""
Habits app views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwner
from .models import Habit
from .serializers import (
    HabitSerializer,
    HabitCreateUpdateSerializer,
    HabitDetailSerializer,
)


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user habits."""
    
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer
    
    def get_queryset(self):
        """Return habits for current user."""
        return Habit.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return HabitCreateUpdateSerializer
        elif self.action == 'retrieve':
            return HabitDetailSerializer
        return HabitSerializer
    
    def perform_create(self, serializer):
        """Create habit with current user."""
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create a new habit."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {
                'message': 'Habit created successfully.',
                'data': HabitSerializer(serializer.instance).data,
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update a habit."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Habit updated successfully.',
                'data': HabitSerializer(serializer.instance).data,
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a habit."""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response(
            {'message': 'Habit deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle habit active status."""
        habit = self.get_object()
        habit.is_active = not habit.is_active
        habit.save()
        
        return Response(
            {
                'message': f'Habit {"activated" if habit.is_active else "deactivated"} successfully.',
                'data': HabitSerializer(habit).data,
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active habits."""
        habits = self.get_queryset().filter(is_active=True)
        serializer = HabitSerializer(habits, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get habit statistics for current user."""
        habits = self.get_queryset()
        
        total_habits = habits.count()
        active_habits = habits.filter(is_active=True).count()
        
        stats = {
            'total_habits': total_habits,
            'active_habits': active_habits,
            'habits': []
        }
        
        for habit in habits:
            stats['habits'].append({
                'id': habit.id,
                'title': habit.title,
                'frequency': habit.frequency,
                'completion_rate': round(habit.get_completion_rate(), 2),
            })
        
        return Response(stats, status=status.HTTP_200_OK)
