Feature: List products by category

  Scenario: List products by category
    Given a valid category id
    When a GET request is sent to "/products"
    Then a list of products for the given category should be returned