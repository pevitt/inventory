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


def create_product(
        *,
        department_id: int,
        name: str,
        description: str,
        code: str,
        cost: float,
        price: float,
        stock: int
) -> 'Dict[str, Any]':
    department_qry = product_selectors.get_department_by_id(
        id=department_id
    )
    product_qry = product_selectors.get_product_by_code(
        code=code
    )

    if product_qry.exists():
        raise InventoryAPIException(ErrorCode.P02)

    department = department_qry.first()
    product = department.products.create(
        department=department,
        name=name,
        description=description,
        code=code,
        cost=cost,
        price=price,
        stock=stock
    )

    product_data = dict(
        id=product.id,
        department=product.department.name,
        name=product.name,
        description=product.description,
        code=product.code,
        cost=product.cost,
        price=product.price,
        stock=product.stock
    )

    return product_data
