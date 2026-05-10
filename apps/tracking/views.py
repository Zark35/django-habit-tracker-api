"""
Tracking app views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q, Count, Case, When, IntegerField
from core.permissions import IsOwner
from .models import HabitEntry
from .serializers import (
    HabitEntrySerializer,
    HabitEntryCreateUpdateSerializer,
    DailyCheckInSerializer,
    HabitEntryDetailSerializer,
)
from apps.habits.models import Habit


class HabitEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing habit entries."""
    
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitEntrySerializer
    
    def get_queryset(self):
        """Return entries for current user's habits."""
        return HabitEntry.objects.filter(
            habit__user=self.request.user
        ).order_by('-completed_date')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return HabitEntryCreateUpdateSerializer
        elif self.action == 'retrieve':
            return HabitEntryDetailSerializer
        elif self.action == 'daily_checkin':
            return DailyCheckInSerializer
        return HabitEntrySerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new habit entry."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                'message': 'Entry created successfully.',
                'data': HabitEntrySerializer(serializer.instance).data,
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update a habit entry."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Entry updated successfully.',
                'data': HabitEntrySerializer(serializer.instance).data,
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a habit entry."""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response(
            {'message': 'Entry deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['post'])
    def daily_checkin(self, request):
        """
        Create or update a daily check-in entry.
        
        Request body:
        {
            "habit_id": 1,
            "status": "completed",
            "notes": "Great progress!",
            "date": "2024-01-15"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        habit_id = serializer.validated_data['habit_id']
        status_value = serializer.validated_data['status']
        notes = serializer.validated_data.get('notes', '')
        date = serializer.validated_data['date']
        
        try:
            entry, created = HabitEntry.objects.update_or_create(
                habit_id=habit_id,
                completed_date=date,
                defaults={'status': status_value, 'notes': notes}
            )
            
            return Response(
                {
                    'message': 'Check-in recorded successfully.',
                    'data': HabitEntrySerializer(entry).data,
                    'created': created,
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's check-in status for all active habits."""
        today = timezone.now().date()
        user_habits = Habit.objects.filter(user=request.user, is_active=True)
        
        today_entries = HabitEntry.objects.filter(
            habit__user=request.user,
            completed_date=today
        )
        
        entries_dict = {entry.habit_id: entry for entry in today_entries}
        
        data = {
            'date': today,
            'entries': []
        }
        
        for habit in user_habits:
            entry = entries_dict.get(habit.id)
            data['entries'].append({
                'habit_id': habit.id,
                'habit_title': habit.title,
                'status': entry.status if entry else None,
                'completed': entry is not None,
            })
        
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def habit_history(self, request):
        """Get entry history for a specific habit."""
        habit_id = request.query_params.get('habit_id')
        days = int(request.query_params.get('days', 30))
        
        if not habit_id:
            return Response(
                {'error': 'habit_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
        except Habit.DoesNotExist:
            return Response(
                {'error': 'Habit not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        start_date = timezone.now().date() - timedelta(days=days)
        entries = HabitEntry.objects.filter(
            habit=habit,
            completed_date__gte=start_date
        ).order_by('-completed_date')
        
        serializer = HabitEntrySerializer(entries, many=True)
        
        return Response(
            {
                'habit_id': habit.id,
                'habit_title': habit.title,
                'period_days': days,
                'entries': serializer.data,
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get tracking statistics for current user."""
        days = int(request.query_params.get('days', 30))
        
        start_date = timezone.now().date() - timedelta(days=days)
        today = timezone.now().date()
        
        entries = HabitEntry.objects.filter(
            habit__user=request.user,
            completed_date__gte=start_date
        )
        
        total_entries = entries.count()
        completed = entries.filter(status='completed').count()
        skipped = entries.filter(status='skipped').count()
        failed = entries.filter(status='failed').count()
        
        completion_rate = (completed / total_entries * 100) if total_entries > 0 else 0
        
        daily_stats = []
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            daily_entries = entries.filter(completed_date=current_date)
            daily_completed = daily_entries.filter(status='completed').count()
            daily_total = daily_entries.count()
            
            daily_stats.append({
                'date': current_date,
                'total': daily_total,
                'completed': daily_completed,
                'rate': (daily_completed / daily_total * 100) if daily_total > 0 else 0,
            })
        
        return Response(
            {
                'period_days': days,
                'total_entries': total_entries,
                'completed': completed,
                'skipped': skipped,
                'failed': failed,
                'overall_completion_rate': round(completion_rate, 2),
                'daily_stats': daily_stats,
            },
            status=status.HTTP_200_OK
        )
