Feature: Browsing sites

    Scenario: Sites must be available at '/browse'
        After I login into the portal
        Given I access the url "/browse/"
        Then I see the heading "All Sites"

    Scenario: Sites list must be paginated
        After I login into the portal
        Given I access the url "/browse/"
        Then I see a div for "pagination pagination-centered "