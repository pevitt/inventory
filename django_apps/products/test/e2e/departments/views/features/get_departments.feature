Feature: Get Departments

Scenario: Get Departments
    Given I request to get all departments
    Then I receive a response with status code 200
    And I recieve a response with 6 departments