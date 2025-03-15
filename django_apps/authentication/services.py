
from typing import Any, Dict
from utils.exceptions import InventoryAPIException, ErrorCode
from .models import Profile
from django_apps.authentication import selectors as auth_selectors
from django.contrib.auth.models import User


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
    token = auth_selectors.get_user_token(user=user)

    if token is None:
        raise InventoryAPIException(ErrorCode.E00)
    data = {
        'token': user.auth_token.key,
    }

    return data
