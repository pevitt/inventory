from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from typing import Any, Dict

from .models import Profile


def create_user(
        *,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str
) -> Profile:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    profile = Profile.objects.create(
        user=user,
        role=role
    )
    return profile


def get_token(user) -> Dict[str, Any]:
    Token.objects.get_or_create(user=user)

    data = {
        'token': user.auth_token.key,
    }

    return data
