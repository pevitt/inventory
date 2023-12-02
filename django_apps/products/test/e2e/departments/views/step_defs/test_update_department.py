from pytest_bdd import given, parsers, scenarios, then, when
from uuid import UUID
import pytest
from django_apps.products import selectors as product_selectors

scenarios('../features/update_department.feature')
ENDPOINT = '/api/products/departments/'


@given(
    parsers.parse(
        'I load all departments'
    ),
    target_fixture='load_all_departments'
)
def load_all_departments(
        db,
        load_departments
):
    """
    Load all departments
    """
    pass


@given(
    parsers.parse(
        'I load all products'
    ),
    target_fixture='load_all_products'
)
def load_all_products(
        db,
        load_products
):
    """
    Load all products
    """
    pass


@when(
    parsers.parse(
        'I request to update department with id {department_id:d} with margin percentage {margin_percentage:f}'
    ),
    target_fixture='api_request'
)
def invoke_update_department(
        db,
        load_all_departments,
        api_client_user_authenticated,
        department_id: int,
        margin_percentage: float
):
    """
    Invoke update department service
    """
    endpoint = f"{ENDPOINT}{department_id}"
    department_data = {
        'margin_percentage': margin_percentage
    }
    return api_client_user_authenticated.put(
        endpoint,
        department_data,
        format='json'
    )


@then(
    parsers.parse(
        'The response status code should be {status_code:d}'
    )
)
def validate_update_department_response(
        api_request,
        status_code: int
):
    """
    Validate update department response
    """
    assert api_request.status_code == status_code

@then(
    parsers.parse(
        'I should see the department with id {department_id:d} with margin percentage {margin_percentage:f}'
    )
)
def validate_department_margin_percentage(
        db,
        department_id: int,
        margin_percentage: float
):
    """
    Validate department margin percentage
    """
    department = product_selectors.get_department_by_id(id=department_id).first()
    assert department.margin_percentage == margin_percentage

@then(
    parsers.parse(
        'I should see the product with id "{product_id}" with price {price:f}'
    )
)
def validate_product_price(
        db,
        product_id: str,
        price: float
):
    """
    Validate product price
    """
    product = product_selectors.get_product_by_id(id=product_id).first()
    assert product.price == price