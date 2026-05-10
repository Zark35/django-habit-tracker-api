import pytest
from rest_framework.test import APIClient

from tests.factories import HabitEntryFactory, HabitFactory, UserFactory


@pytest.fixture
def api_client():
    """Return a DRF APIClient instance for unauthenticated requests."""
    return APIClient()


@pytest.fixture
def user():
    """Create a default user for authenticated test scenarios."""
    return UserFactory()


@pytest.fixture
def another_user():
    """Create a second user for authorization/security tests."""
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client, user):
    """Return a client already authenticated as the default user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def habit(user):
    """Create a habit owned by the authenticated user."""
    return HabitFactory(user=user)


@pytest.fixture
def habit_entry(habit):
    """Create a habit entry linked to the authenticated user's habit."""
    return HabitEntryFactory(habit=habit)
