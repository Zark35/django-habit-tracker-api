"""
Habits app admin configuration.
"""

from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Admin configuration for Habit model."""
    
    list_display = ('title', 'user', 'frequency', 'is_active', 'created_at')
    list_filter = ('frequency', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Habit Info', {'fields': ('user', 'title', 'description')}),
        ('Configuration', {'fields': ('frequency', 'target_count', 'icon', 'color')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
