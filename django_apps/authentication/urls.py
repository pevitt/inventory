from django.urls import include, path

from .views import LoginView, SignUPView

urlpatterns = [
    path(
        'signup',
        SignUPView.as_view(),
        name='signup'
    ),
    path(
        'login',
        LoginView.as_view(),
        name='login'
    )
]