from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/create_product.feature')
ENDPOINT = '/api/products/'

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

@then(
    parsers.parse(
        'I invoke service to create product with name {name} and description {description} and department_id '
        '{department_id} and code {code} and cost {cost}'
    ),
    target_fixture='api_request'
)
def invoke_create_product(
    db,
    load_all_departments,
    api_client_user_authenticated,
    name: str,
    description: str,
    department_id: int,
    code: str,
    cost: float
):
    """
    Invoke create product service
    """
    endpoint = f"{ENDPOINT}"
    data = {
        'name': name,
        'description': description,
        'department_id': department_id,
        'code': code,
        'cost': cost
    }
    return api_client_user_authenticated.post(
        endpoint,
        data,
        format='json'
    )

@then(
    parsers.parse(
        'The response of the service should be status code {status_code:d}'
    )
)
def validate_status_response(
    api_request,
    status_code: int
):
    """
    Validate status response
    """
    assert api_request.status_code == status_code

@then(
    parsers.parse(
        'The product must be created with price {price:f}'
    )
)
def validate_product_price(
    api_request,
    price: float
):
    """
    Validate product price
    """
    assert api_request.data['price'] == price
