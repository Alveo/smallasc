Feature: Search for items

    Scenario: Search must present the correct title
        After I login into the portal
        Given I access the url "/search/"
        Then I see the heading "Corpus Search"

    Scenario: Search must present a gender field as first field
        After I login into the portal
        Given I access the url "/search/"
        Then I see that label 1 is "Gender"

    Scenario: Search must present a socio economic status as second field
        After I login into the portal
        Given I access the url "/search/"
        Then I see that label 2 is "Socio Economic Status"

    Scenario: Search must present a highest qualification as third field
        After I login into the portal
        Given I access the url "/search/"
        Then I see that label 3 is "Highest Qualification"

    Scenario: Search must present a professional category as fourth field
        After I login into the portal
        Given I access the url "/search/"
        Then I see that label 4 is "Professional Category"

    