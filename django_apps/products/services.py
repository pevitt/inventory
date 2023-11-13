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
