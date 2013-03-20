Feature: Browsing sites

    Scenario: Sites must be available at '/browse'
        After I login into the portal
        Given I access the url "/browse/"
        Then I see the heading "Sites"

    Scenario: Sites list must be paginated
        After I login into the portal
        Given I access the url "/browse/"
        Then I see a div for "pagination pagination-centered "

    Scenario: Sites must include a male participant count 
        After I login into the portal
        Given I access the url "/browse/"
        Then I see that "sites summary" paragraph 1 is "male participants"

    Scenario: Sites must include a female participant count 
        After I login into the portal
        Given I access the url "/browse/"
        Then I see that "sites summary" paragraph 2 is "female participants"

    Scenario: Sites must include a total participant count 
        After I login into the portal
        Given I access the url "/browse/"
        Then I see that "sites summary" paragraph 3 is "total participants"

    Scenario: Sites must include a link to browse specific site participants 
        After I login into the portal
        Given I access the url "/browse/"
        Then I see that link 9 is "/browse/UWA/"
