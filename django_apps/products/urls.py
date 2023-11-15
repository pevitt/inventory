from django.urls import include, path
from .views import DepartmentView, DepartmentDetailView, ProductView, ProductViewDetail

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
    ),
    path(
        '<uuid:product_id>',
        ProductViewDetail.as_view(),
        name='products'
    )
]