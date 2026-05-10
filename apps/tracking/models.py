"""
Tracking app models.
"""

from django.db import models
from django.contrib.auth import get_user_model
from apps.habits.models import Habit

User = get_user_model()


class HabitEntry(models.Model):
    """Model for tracking daily habit entries/check-ins."""
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
        ('failed', 'Failed'),
    ]
    
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='entries')
    completed_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'habit_entries'
        ordering = ['-completed_date']
        unique_together = ('habit', 'completed_date')
        indexes = [
            models.Index(fields=['habit', 'completed_date']),
            models.Index(fields=['status']),
            models.Index(fields=['completed_date']),
        ]
    
    def __str__(self):
        return f'{self.habit.title} - {self.completed_date} ({self.status})'
    
    @property
    def user(self):
        """Get the user associated with this entry."""
        return self.habit.user
