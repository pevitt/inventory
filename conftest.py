import pytest
from mixer.backend.django import mixer

from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from django_apps.authentication.models import Profile


@pytest.fixture
def api_client() -> APIClient:
    """
    API Client to consume services
    """
    client = APIClient()
    return client


@pytest.fixture
def create_user_profile(db) -> User:
    """
    User fixture
    """
    user = mixer.blend(
        User,
        username=mixer.faker.pystr(),
        email="jrigoberto17@gmail.com",
        password="123456",
        first_name="Jose",
        last_name="Rigoberto"
    )

    profile = mixer.blend(
        Profile,
        user=user,
        role="admin"
    )

    return user

@pytest.fixture
def api_client_user_authenticated(
        db,
        api_client,
        create_user_profile
) -> APIClient:
    """
    API Client to consume services
    """
    user = create_user_profile
    # import pdb; pdb.set_trace()
    token = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
    return api_client

@pytest.fixture
def load_departments(db):
    """
    Load departments from fixtures to departments table
    """
    call_command('loaddata', 'fixtures/departments.json')
