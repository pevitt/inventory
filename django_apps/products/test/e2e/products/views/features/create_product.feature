Feature: Create products with multiple variants

Scenario Outline: Create products success
    Given I load all departments
    Then I invoke service to create product with name <name> and description <description> and department_id <department_id> and code <code> and cost <cost>
    Then The response of the service should be status code <status_code>
    And The product must be created with price <price>

    Examples:
        | name | description | department_id | code | cost | price | status_code |
        | Product 1 | Description 1 | 1 | 123 | 10 | 13.0 | 201 |
        | Product 2 | Description 2 | 2 | 123 | 10 | 13.0 | 201 |
        | Product 3 | Description 3 | 3 | 123 | 10 | 13.0 | 201 |
        | Product 4 | Description 4 | 4 | 123 | 10 | 13.0 | 201 |
        | Product 5 | Description 5 | 5 | 123 | 10 | 13.0 | 201 |
        | Product 6 | Description 6 | 6 | 123 | 10 | 15.0 | 201 |