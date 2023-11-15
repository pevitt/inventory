from .models import Departments, Products
from django.db.models import QuerySet
from uuid import UUID

def get_departments_list() -> 'QuerySet[Departments]':
    departments = Departments.objects.all()
    return departments


def get_department_by_id(
        *,
        id: int
) -> 'QuerySet[Departments]':
    departments = Departments.objects.filter(
        pk=id
    )
    return departments


def get_product_by_code(
        *,
        code: str
) -> 'QuerySet[Products]':
    products = Products.objects.filter(
        code=code
    )
    return products


def get_product_by_id(
        *,
        id: UUID
) -> 'QuerySet[Products]':
    products = Products.objects.filter(
        pk=id
    )
    return products
