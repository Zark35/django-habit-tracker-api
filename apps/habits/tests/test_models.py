import pytest

from apps.habits.models import Habit
from tests.factories import HabitEntryFactory


@pytest.mark.django_db
def test_get_completion_rate_without_entries_returns_zero(habit):
    assert habit.get_completion_rate() == 0


@pytest.mark.django_db
def test_get_completion_rate_computes_percentage(habit):
    HabitEntryFactory(habit=habit, status='completed')
    HabitEntryFactory(habit=habit, status='failed')

    assert habit.get_completion_rate() == 50.0
