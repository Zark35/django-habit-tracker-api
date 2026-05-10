import datetime

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from apps.habits.models import Habit
from apps.tracking.models import HabitEntry
from apps.users.models import User


class UserFactory(DjangoModelFactory):
    """Factory for the custom User model."""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')


class HabitFactory(DjangoModelFactory):
    """Factory for user habits."""

    class Meta:
        model = Habit

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'Test Habit {n}')
    description = 'Test habit description.'
    frequency = 'daily'
    icon = '🏃'
    color = '#3498db'
    target_count = 1
    is_active = True


class HabitEntryFactory(DjangoModelFactory):
    """Factory for daily habit tracking entries."""

    class Meta:
        model = HabitEntry

    habit = factory.SubFactory(HabitFactory)
    completed_date = factory.Sequence(lambda n: timezone.now().date() - datetime.timedelta(days=n))
    status = 'completed'
    notes = 'Test check-in entry.'
