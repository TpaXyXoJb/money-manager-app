import pytest
from .factories import UserFactory
from ..models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user_registration(api_client):
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testuserpassword123',
    }
    response = api_client.post(reverse('user_create'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'username' in response.data
    assert 'email' in response.data


@pytest.mark.django_db
def test_user_registration_missing(api_client):
    data = {
        'username': 'testuser',
    }
    response = api_client.post(reverse('user_create'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data
    assert 'password' in response.data


@pytest.mark.django_db
def test_obtain_tokens(test_user, api_client):
    data = {
        'email': test_user.email,
        'password': 'testuserpassword123',
    }
    response = api_client.post(reverse('token_obtain_pair'), data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_authorization_with_token(test_user, api_client):
    data = {
        'email': test_user.email,
        'password': 'testuserpassword123',
    }
    token_response = api_client.post(reverse('token_obtain_pair'), data)
    access_token = token_response.data['access']

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(reverse('user_summary'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == test_user.username


@pytest.mark.django_db
def test_authorization_with_invalid_data(test_user, api_client):
    data = {
        'email': 'wrongemail@test.com',
        'password': 'testuserpassword123'
    }
    response = api_client.post(reverse('token_obtain_pair'), data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access' not in response.data
    assert 'refresh' not in response.data

    data = {
        'email': test_user.email,
        'password': 'wrongpassword123',
    }
    response = api_client.post(reverse('token_obtain_pair'), data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access' not in response.data
    assert 'refresh' not in response.data


@pytest.mark.django_db
def test_get_user_data_unauthorized(api_client):
    response = api_client.get(reverse('user_summary'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
