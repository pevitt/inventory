from django.urls import include, path
from .views import DepartmentView, DepartmentDetailView, ProductView

urlpatterns = [
    path(
        'departments',
        DepartmentView.as_view(),
        name='departments'
    ),
    path(
        'departments/<int:department_id>',
        DepartmentDetailView.as_view(),
        name='department_detail'
    ),
    path(
        '',
        ProductView.as_view(),
        name='products'
    )
]