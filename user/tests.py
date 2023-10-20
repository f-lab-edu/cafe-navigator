import pytest
from user.models import User
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture(scope='session')
def user_fixture(db):
    return User.objects.create_user(
        'testuser', 'testpassword'
    )


def test_superuser_view(admin_client):
    url = reverse('user-list')
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_unauthenticated_user_view(api_client):
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize(
   'username, password, status_code', [
    #    (None, None, 400),
    #    (None, 'strong_pass', 400),
    #    ('user@example.com', None, 400),
    #    ('user@example.com', 'invalid_pass', 400),
       ('user@example.com', 'strong_pass', 201),
   ]
)
def test_signup_data_validation(
   username, password, status_code, api_client
):
    url = reverse('user-signup')
    data = {
        'username': username,
        'password': password
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
   'username, password, status_code', [
       ('testuser', 'invalid_pass', 404),
    #    ('testuser', 'testpassword', 200),
   ]
)
def test_login(
   username, password, status_code, api_client
):
    url = reverse('user-login')
    data = {
        'username': username,
        'password': password
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status_code