Feature: Search for items

    Scenario: Search must present the correct title
        After I login into the portal
        Given I access the url "/search/"
        Then I see the heading "Corpus Search"