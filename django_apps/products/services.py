import uuid

from django_apps.products import selectors as product_selectors
from typing import Any, Dict
from utils.exceptions import InventoryAPIException, ErrorCode
from django.db.models import F
from decimal import Decimal
from uuid import UUID
from django.db import transaction


def get_all_departments() -> 'Dict[str, Any]':
    """
    Get all departments
    :return:
    """
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
    """
    Get department by id
    :param department_id:
    :return:
    """
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
    """
    Update department
    :param department_id:
    :param margin_percentage:
    :return:
    """
    department_qry = product_selectors.get_department_by_id(
        id=department_id
    )

    if not department_qry.exists():
        raise InventoryAPIException(ErrorCode.D01)

    department = department_qry.first()
    department.margin_percentage = margin_percentage
    department.save()

    update_price_products_by_department_orm(department=department)

    department_data = dict(
        id=department.id,
        name=department.name,
        description=department.description,
        code=department.code,
        margin_percentage=department.margin_percentage
    )

    return department_data


def update_price_products_by_department(
        department: 'Departments'
):
    """
    Update price products by department
    :param department:
    :return:
    """
    products = department.products.all()

    for product in products:
        product.price = Decimal(product.cost) + (Decimal(product.cost) * Decimal(department.margin_percentage / 100))
        product.save()


def update_price_products_by_department_orm(
        department: 'Departments'
):
    """
    Update price products by department
    :param department:
    :return:
    """
    products = department.products.all()

    products.update(
        price=F('cost') + (F('cost') * (department.margin_percentage / 100))
    )


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
    """
    Create product
    :param department_id:
    :param name:
    :param description:
    :param code:
    :param cost:
    :param price:
    :param stock:
    :return:
    """
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


def get_products_by_department_id(
        *,
        department_id: int
) -> 'Dict[str, Any]':
    """
    Get products by department id
    :param department_id:
    :return:
    """
    department_qry = product_selectors.get_department_by_id(
        id=department_id
    )

    if not department_qry.exists():
        raise InventoryAPIException(ErrorCode.D01)

    department = department_qry.first()
    products = department.products.all()

    data_products = products.annotate(
        department_name=F('department__name')
    ).values(
        'id',
        'department_name',
        'name',
        'description',
        'code',
        'cost',
        'price',
        'stock'
    )

    return list(data_products)


def get_product_by_id(
        *,
        product_id: UUID,
) -> 'Dict[str, Any]':
    """
    Get product by id
    :param product_id:
    :return:
    """
    product_qry = product_selectors.get_product_by_id(
        id=product_id
    )

    if not product_qry.exists():
        raise InventoryAPIException(ErrorCode.P01)

    product = product_qry.first()

    product_data = dict(
        id=product.id,
        department_name=product.department.name,
        name=product.name,
        description=product.description,
        code=product.code,
        cost=product.cost,
        price=product.price,
        stock=product.stock
    )

    return product_data


def update_product(
        *,
        product_id: UUID,
        id: UUID,
        name: str,
        description: str,
        cost: float,
        stock: int
) -> 'Dict[str, Any]':
    """
    Update product
    :param product_id:
    :param name:
    :param description:
    :param code:
    :param cost:
    :param price:
    :param stock:
    :return:
    """
    product_qry = product_selectors.get_product_by_id(
        id=product_id
    )

    if not product_qry.exists():
        raise InventoryAPIException(ErrorCode.P01)

    product = product_qry.first()
    product.name = name
    product.description = description
    product.cost = cost
    product.stock = stock
    product.save()

    product_data = dict(
        id=product.id,
        department_name=product.department.name,
        name=product.name,
        description=product.description,
        code=product.code,
        cost=product.cost,
        price=product.price,
        stock=product.stock
    )

    return product_data


def create_purchase_order(
        *,
        product_id: uuid,
        quantity: int,
        unit_cost: float,
        total_cost: float
) -> 'Dict[str, Any]':
    """
    Create purchase order
    :param product_id:
    :param quantity:
    :param unit_cost:
    :param total_cost:
    :return:
    """
    product_qry = product_selectors.get_product_by_id(
        id=product_id
    )

    if not product_qry.exists():
        raise InventoryAPIException(ErrorCode.P01)

    product = product_qry.first()

    purchase_order_data = dict()

    with transaction.atomic():
        product.stock = product.stock + quantity
        product.cost = unit_cost
        product.save()

        purchase_order = product.purchase_order_product.create(
            product=product,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=total_cost
        )

        purchase_order_data = dict(
            id=purchase_order.id,
            product_name=purchase_order.product.name,
            quantity=purchase_order.quantity,
            unit_cost=purchase_order.unit_cost,
            total_cost=purchase_order.total_cost,
            purchase_date=purchase_order.purchase_date,
            status=purchase_order.status
        )

        return purchase_order_data


def create_sale_order(
        *,
        product_id: uuid,
        quantity: int,
        unit_price: float,
        total_price: float
) -> 'Dict[str, Any]':
    """
    Create sale order
    :param product_id:
    :param quantity:
    :param unit_price:
    :param total_price:
    :return:
    """
    product_qry = product_selectors.get_product_by_id(
        id=product_id
    )

    if not product_qry.exists():
        raise InventoryAPIException(ErrorCode.P01)

    product = product_qry.first()

    sale_order_data = dict()

    with transaction.atomic():
        product.stock = product.stock - quantity
        product.save()

        sale_order = product.sale_order_product.create(
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )

        sale_order_data = dict(
            id=sale_order.id,
            product_name=sale_order.product.name,
            quantity=sale_order.quantity,
            unit_price=sale_order.unit_price,
            total_price=sale_order.total_price,
            sale_date=sale_order.sale_date,
            status=sale_order.status
        )

    return sale_order_data
