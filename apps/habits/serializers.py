"""
Habits app serializers.
"""

from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Serializer for Habit model."""
    
    completion_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Habit
        fields = [
            'id', 'title', 'description', 'frequency', 'icon', 'color',
            'target_count', 'is_active', 'completion_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_completion_rate(self, obj):
        """Get completion rate for the habit."""
        return round(obj.get_completion_rate(), 2)


class HabitCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating habits."""
    
    class Meta:
        model = Habit
        fields = [
            'title', 'description', 'frequency', 'icon', 'color',
            'target_count', 'is_active'
        ]
    
    def validate_title(self, value):
        """Validate that title is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError('Title cannot be empty.')
        return value.strip()
    
    def validate_target_count(self, value):
        """Validate target count is positive."""
        if value < 1:
            raise serializers.ValidationError('Target count must be at least 1.')
        return value
    
    def validate_frequency(self, value):
        """Validate frequency choice."""
        valid_frequencies = ['daily', 'weekly', 'monthly']
        if value not in valid_frequencies:
            raise serializers.ValidationError(
                f'Frequency must be one of: {", ".join(valid_frequencies)}'
            )
        return value


class HabitDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for habit information."""
    
    completion_rate = serializers.SerializerMethodField()
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    
    class Meta:
        model = Habit
        fields = [
            'id', 'title', 'description', 'frequency', 'frequency_display',
            'icon', 'color', 'target_count', 'is_active', 'completion_rate',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_completion_rate(self, obj):
        """Get completion rate for the habit."""
        return round(obj.get_completion_rate(), 2)
