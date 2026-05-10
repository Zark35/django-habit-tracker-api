import pytest
from apps.habits.serializers import HabitCreateUpdateSerializer


@pytest.mark.django_db
def test_habit_serializer_rejects_empty_title():
    serializer = HabitCreateUpdateSerializer(data={
        'title': '   ',
        'description': 'Empty title should fail',
        'frequency': 'daily',
        'icon': '📝',
        'color': '#3498db',
        'target_count': 1,
        'is_active': True,
    })

    assert not serializer.is_valid()
    assert 'title' in serializer.errors


@pytest.mark.django_db
def test_habit_serializer_rejects_invalid_frequency():
    serializer = HabitCreateUpdateSerializer(data={
        'title': 'Healthy Eating',
        'description': 'Eat a salad every day',
        'frequency': 'yearly',
        'icon': '🥗',
        'color': '#2ecc71',
        'target_count': 1,
        'is_active': True,
    })

    assert not serializer.is_valid()
    assert 'frequency' in serializer.errors
