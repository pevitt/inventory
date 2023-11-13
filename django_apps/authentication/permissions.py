from rest_framework import permissions
from django_apps.authentication import selectors as users_selectors

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        profile = users_selectors.get_user_profile(user=request.user)
        return profile.role == 'admin'


class IsSalesUser(permissions.BasePermission):
    """
    Allows access only to sales users.
    """

    def has_permission(self, request, view):
        profile = users_selectors.get_user_profile(user=request.user)
        return profile.role == 'sales'


class IsPurchaseUser(permissions.BasePermission):
    """
    Allows access only to purchase users.
    """

    def has_permission(self, request, view):
        profile = users_selectors.get_user_profile(user=request.user)
        return profile.role == 'purchase'
