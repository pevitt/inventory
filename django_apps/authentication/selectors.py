from django.db.models import QuerySet
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Profile


def filter_user_by_email(
        *,
        email: str
) -> 'QuerySet[User]':
    return User.objects.filter(
        email=email
    )


def get_user_profile(
        *,
        user: User
) -> 'QuerySet[Profile]':
    return Profile.objects.get(
        user=user
    )


def filter_by_names(
        *,
        first_name: str,
        last_name: str
) -> 'QuerySet[User]':
    return User.objects.filter(
        first_name=first_name,
        last_name=last_name
    )

def get_user_token(
        *,
        user: User
) -> 'QuerySet[Token]':
    return Token.objects.get_or_create(
        user=user
    )
