from pytest_bdd import given, parsers, scenarios, then

scenarios('../features/get_departments.feature')
ENDPOINT = '/api/products/departments'

@given(
    parsers.parse(
        'I request to get all departments'
    ),
    target_fixture='api_request'
)
def invoke_get_departments(
        db,
        api_client_user_authenticated,
        load_departments
):
    """
    Invoke get departments service
    """
    return api_client_user_authenticated.get(
        ENDPOINT,
        format='json'
    )

@then(
    parsers.parse(
        'I receive a response with status code {status_code:d}'
    )
)
def validate_get_departments_response(
        api_request,
        status_code: int
):
    """
    Validate get departments response
    """
    assert api_request.status_code == status_code

@then(
    parsers.parse(
        'I recieve a response with {count:d} departments'
    )
)
def validate_count_departments(
        api_request,
        count: int
):
    """
    Validate count departments
    """
    assert len(api_request.data) == count