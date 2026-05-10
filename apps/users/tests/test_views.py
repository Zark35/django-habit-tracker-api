import pytest
from rest_framework import status


@pytest.mark.django_db
def test_user_registration_creates_user(api_client):
    payload = {
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'password': 'testpassword123',
        'password_confirm': 'testpassword123',
    }
    response = api_client.post('/api/auth/register/', payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['user']['email'] == 'newuser@example.com'


@pytest.mark.django_db
def test_jwt_login_returns_tokens(api_client, user):
    payload = {
        'email': user.email,
        'password': 'testpassword123',
    }
    response = api_client.post('/api/auth/login/', payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'tokens' in response.data
    assert 'access' in response.data['tokens']
    assert 'refresh' in response.data['tokens']


@pytest.mark.django_db
def test_token_refresh_returns_new_access_token(api_client, user):
    login_response = api_client.post(
        '/api/auth/login/',
        {'email': user.email, 'password': 'testpassword123'},
        format='json'
    )

    refresh_token = login_response.data['tokens']['refresh']
    refresh_response = api_client.post(
        '/api/auth/refresh_token/',
        {'refresh': refresh_token},
        format='json'
    )

    assert refresh_response.status_code == status.HTTP_200_OK
    assert 'access' in refresh_response.data


@pytest.mark.django_db
def test_login_with_invalid_credentials_returns_400(api_client, user):
    response = api_client.post(
        '/api/auth/login/',
        {'email': user.email, 'password': 'wrongpassword'},
        format='json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Invalid email or password.' in str(response.data)


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_protected_endpoint(api_client):
    response = api_client.get('/api/habits/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
