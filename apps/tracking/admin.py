"""
Tracking app admin configuration.
"""

from django.contrib import admin
from .models import HabitEntry


@admin.register(HabitEntry)
class HabitEntryAdmin(admin.ModelAdmin):
    """Admin configuration for HabitEntry model."""
    
    list_display = ('habit', 'completed_date', 'status', 'created_at')
    list_filter = ('status', 'completed_date', 'created_at')
    search_fields = ('habit__title', 'habit__user__email', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-completed_date',)
    
    fieldsets = (
        ('Entry Info', {'fields': ('habit', 'completed_date', 'status')}),
        ('Additional Info', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
