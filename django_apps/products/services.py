from django_apps.products import selectors as product_selectors
from typing import Any, Dict
from utils.exceptions import InventoryAPIException, ErrorCode


def get_all_departments() -> 'Dict[str, Any]':
    departments = product_selectors.get_departments_list()

    data_departments = departments.values(
        'id',
        'name',
        'description',
        'code',
        'margin_percentage'
    )

    return list(data_departments)


def get_department_by_id(
        *,
        department_id: int
) -> 'Dict[str, Any]':
    department_qry = product_selectors.get_department_by_id(
        id=department_id
    )

    if not department_qry.exists():
        raise InventoryAPIException(ErrorCode.D01)

    return department_qry.first()


def update_department(
        *,
        department_id: int,
        margin_percentage: float
) -> 'Dict[str, Any]':
    department_qry = product_selectors.get_department_by_id(
        id=department_id
    )

    if not department_qry.exists():
        raise InventoryAPIException(ErrorCode.D01)

    department = department_qry.first()
    department.margin_percentage = margin_percentage
    department.save()

    department_data = dict(
        id=department.id,
        name=department.name,
        description=department.description,
        code=department.code,
        margin_percentage=department.margin_percentage
    )

    return department_data
