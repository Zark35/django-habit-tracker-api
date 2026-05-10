import pytest
from django.utils import timezone
from rest_framework import status

from tests.factories import HabitEntryFactory, HabitFactory


@pytest.mark.django_db
def test_create_tracking_entry(authenticated_client, habit):
    payload = {
        'habit': habit.id,
        'completed_date': timezone.now().date().isoformat(),
        'status': 'completed',
        'notes': 'Completed my habit today.',
    }

    response = authenticated_client.post('/api/tracking/', payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['data']['habit'] == habit.id
    assert response.data['data']['status'] == 'completed'


@pytest.mark.django_db
def test_prevent_duplicate_entries_for_same_date(authenticated_client, habit):
    date = timezone.now().date()
    HabitEntryFactory(habit=habit, completed_date=date)

    duplicate_payload = {
        'habit': habit.id,
        'completed_date': date.isoformat(),
        'status': 'completed',
        'notes': 'Duplicate entry attempt.',
    }

    response = authenticated_client.post('/api/tracking/', duplicate_payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data


@pytest.mark.django_db
def test_authenticated_access_only(api_client):
    response = api_client.get('/api/tracking/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_cannot_create_entry_for_other_users_habit(authenticated_client, another_user):
    other_habit = HabitFactory(user=another_user)
    payload = {
        'habit': other_habit.id,
        'completed_date': timezone.now().date().isoformat(),
        'status': 'completed',
        'notes': 'Trying to write other user entry.',
    }

    response = authenticated_client.post('/api/tracking/', payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data
