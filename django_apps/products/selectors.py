from .models import Departments, Products
from django.db.models import QuerySet


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
