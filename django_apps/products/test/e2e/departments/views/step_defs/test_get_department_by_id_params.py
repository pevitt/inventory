from pytest_bdd import given, parsers, scenarios, then
import pytest

scenarios('../features/get_department_by_id_params.feature')
ENDPOINT = '/api/products/departments/'

@given(
    parsers.parse(
        'I load all departments'
    ),
    target_fixture='load_all_departments'
)
@pytest.mark.skip(reason="Not implemented yet")
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
        'I request department by id {department_id}'
    ),
    target_fixture='api_request'
)
def invoke_get_department_by_id(
        db,
        load_all_departments,
        api_client_user_authenticated,
        department_id
):
    """
    Invoke get department by id service
    """
    print(f"Department id: {department_id}")
    #import pdb; pdb.set_trace()
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
        status_code
):
    """
    Validate get department by id response
    """
    breakpoint()  # Esto usará pdb++ automáticamente
    assert api_request.status_code == status_code

@then(
    parsers.parse(
        'I get a department named {name}'
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