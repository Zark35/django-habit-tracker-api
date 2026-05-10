import pytest
from rest_framework import status

from tests.factories import HabitFactory


@pytest.mark.django_db
def test_create_habit(authenticated_client):
    payload = {
        'title': 'Morning Journal',
        'description': 'Write a short journal entry every morning.',
        'frequency': 'daily',
        'icon': '📝',
        'color': '#1abc9c',
        'target_count': 1,
        'is_active': True,
    }

    response = authenticated_client.post('/api/habits/', payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['data']['title'] == payload['title']


@pytest.mark.django_db
def test_list_returns_only_current_user_habits(authenticated_client, user, another_user):
    HabitFactory(user=user, title='User Habit')
    HabitFactory(user=another_user, title='Other User Habit')

    response = authenticated_client.get('/api/habits/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'User Habit'


@pytest.mark.django_db
def test_update_own_habit(authenticated_client, habit):
    payload = {
        'title': 'Updated Habit Title',
    }

    response = authenticated_client.patch(f'/api/habits/{habit.id}/', payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['title'] == payload['title']


@pytest.mark.django_db
def test_delete_own_habit(authenticated_client, habit):
    response = authenticated_client.delete(f'/api/habits/{habit.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_cannot_access_other_users_habit(authenticated_client, another_user):
    other_habit = HabitFactory(user=another_user)

    response = authenticated_client.get(f'/api/habits/{other_habit.id}/')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_habit_creation_validation_errors(authenticated_client):
    payload = {
        'title': '   ',
        'description': 'Invalid title only spaces',
        'frequency': 'invalid-frequency',
        'icon': '🏃',
        'color': '#1abc9c',
        'target_count': 0,
        'is_active': True,
    }

    response = authenticated_client.post('/api/habits/', payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'title' in response.data
    assert 'frequency' in response.data
    assert 'target_count' in response.data
