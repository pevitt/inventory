Feature: Update department Margin

Scenario: Update department Margin Successfully
    Given I load all departments
    And I load all products
    When I request to update department with id 1 with margin percentage 10.0
    Then The response status code should be 202
    Then I should see the department with id 1 with margin percentage 10.0
    And I should see the product with id "5fe3f3ed-e6b0-4b38-8c31-0efb9b70c18e" with price 33.0