from pytest_bdd import given, parsers, scenarios, then

scenarios('../features/get_department_by_id.feature')
ENDPOINT = '/api/products/departments/'

@given(
    parsers.parse(
        'I load all deparments'
    ),
    target_fixture='load_all_departments'
)
def load_departements(
        db,
        load_departments
):
    """
    Load all departments
    """
    pass

@then(
    parsers.parse(
        'I request department by id {department_id:d}'
    ),
    target_fixture='api_request'
)
def invoke_get_department_by_id(
        db,
        api_client_user_authenticated,
        department_id
):
    """
    Invoke get department by id service
    """
    endpoint = f"{ENDPOINT}{department_id}"
    return api_client_user_authenticated.get(
        endpoint,
        format='json'
    )

@then(
    parsers.parse(
        'I receive a response with status code {status_code:d}'
    )
)
def validate_get_department_by_id_response(
        api_request,
        status_code: int
):
    """
    Validate get department by id response
    """
    assert api_request.status_code == status_code

@then(
    parsers.parse(
        'I get a department named "{name}"'
    )
)
def validate_department_name(
        api_request,
        name: str
):
    """
    Validate department name
    """
    assert api_request.data['name'] == name

@then(
    parsers.parse(
        'I get a message "{message}"'
    )
)
def validate_message(
        api_request,
        message: str
):
    """
    Validate message
    """
    #import pdb; pdb.set_trace()
    assert api_request.data['detail'] == message