from django.urls import include, path
from .views import DepartmentView

urlpatterns = [
    path(
        'departments',
        DepartmentView.as_view(),
        name='departments'
    )
]