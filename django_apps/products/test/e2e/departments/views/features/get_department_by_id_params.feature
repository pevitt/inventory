Feature: Get Departments by Id Params

Scenario Outline: Get Departments by Id Params Successfully
    Given I load all departments
    Then I request department by id <department_id>
    Then I receive a response with status code <status_code>
    And I get a department named <name>

    Examples:
    | department_id | status_code | name |
    | 1             | 200         | Carniceria   |
    | 2             | 200         | Fruver   |
    | 3             | 200         | Licores   |
    | 4             | 200         | Importados   |
    | 5             | 200         | Refrigerados   |
    | 6             | 200         | Mariscos   |


