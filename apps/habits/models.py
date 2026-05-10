"""
Habits app models.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Habit(models.Model):
    """Model for tracking user habits."""
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    icon = models.CharField(max_length=50, blank=True, default='')
    color = models.CharField(max_length=7, blank=True, default='#3498db')
    target_count = models.IntegerField(default=1, help_text='Target number of completions per frequency period')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'habits'
        ordering = ['-created_at']
        unique_together = ('user', 'title')
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f'{self.user.email} - {self.title}'
    
    def get_completion_rate(self):
        """Calculate completion rate for the last 7 days."""
        from django.utils import timezone
        from datetime import timedelta
        
        last_7_days = timezone.now() - timedelta(days=7)
        total_entries = self.entries.filter(
            created_at__gte=last_7_days
        ).count()
        
        if total_entries == 0:
            return 0
        
        completed_entries = self.entries.filter(
            created_at__gte=last_7_days,
            status='completed'
        ).count()
        
        return (completed_entries / total_entries) * 100
