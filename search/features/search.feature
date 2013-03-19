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

    Scenario: The first step in a search is to Find Speakers
        After I login into the portal
        Given I access the url "/search/"
        Then I see the button "Find Speakers"

    Scenario: The second step in a search is to Find Items
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin"
        Then I see the button "Find Items"

    Scenario: Search must list the number of participants that match the search criteria
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin"
        Then I see that paragraph 1 is "Found 3 participant(s)."