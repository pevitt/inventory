Feature: Get Departments by Id

Scenario: Get Departments by Id Successfully
    Given I load all deparments
    Then I request department by id 1
    Then I receive a response with status code 200
    And I get a department named "Carniceria"

Scenario: Get Departments by Id Not Found
    Given I load all deparments
    Then I request department by id 100
    Then I receive a response with status code 404
    And I get a message "Department does not exist."
