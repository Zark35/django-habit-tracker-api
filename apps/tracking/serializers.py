"""
Tracking app serializers.
"""

from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from .models import HabitEntry
from apps.habits.models import Habit


class HabitEntrySerializer(serializers.ModelSerializer):
    """Serializer for HabitEntry model."""
    
    habit_title = serializers.CharField(source='habit.title', read_only=True)
    
    class Meta:
        model = HabitEntry
        fields = ['id', 'habit', 'habit_title', 'completed_date', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class HabitEntryCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating habit entries."""
    
    class Meta:
        model = HabitEntry
        fields = ['habit', 'completed_date', 'status', 'notes']
    
    def validate_completed_date(self, value):
        """Validate that completed date is not in the future."""
        if value > timezone.now().date():
            raise serializers.ValidationError('Completed date cannot be in the future.')
        return value
    
    def validate_status(self, value):
        """Validate status choice."""
        valid_statuses = ['completed', 'skipped', 'failed']
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f'Status must be one of: {", ".join(valid_statuses)}'
            )
        return value
    
    def validate(self, data):
        """Validate that habit belongs to current user."""
        habit = data.get('habit')
        user = self.context['request'].user
        
        if habit.user != user:
            raise serializers.ValidationError(
                'You can only create entries for your own habits.'
            )
        
        return data


class DailyCheckInSerializer(serializers.Serializer):
    """Serializer for daily check-in data."""
    
    habit_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=['completed', 'skipped', 'failed'])
    notes = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(required=False)
    
    def validate_habit_id(self, value):
        """Validate that habit exists."""
        try:
            Habit.objects.get(id=value)
        except Habit.DoesNotExist:
            raise serializers.ValidationError('Habit not found.')
        return value
    
    def validate(self, data):
        """Validate check-in data."""
        habit = Habit.objects.get(id=data['habit_id'])
        user = self.context['request'].user
        
        if habit.user != user:
            raise serializers.ValidationError(
                'You can only create entries for your own habits.'
            )
        
        date = data.get('date', timezone.now().date())
        if date > timezone.now().date():
            raise serializers.ValidationError('Check-in date cannot be in the future.')
        
        data['date'] = date
        return data


class EntryStatsSerializer(serializers.Serializer):
    """Serializer for entry statistics."""
    
    date = serializers.DateField()
    total_entries = serializers.IntegerField()
    completed = serializers.IntegerField()
    skipped = serializers.IntegerField()
    failed = serializers.IntegerField()
    completion_rate = serializers.FloatField()


class HabitEntryDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for habit entry information."""
    
    habit_title = serializers.CharField(source='habit.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = HabitEntry
        fields = ['id', 'habit', 'habit_title', 'completed_date', 'status', 'status_display', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
