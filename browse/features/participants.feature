Feature: Browsing participants

    Scenario: Participants must be available at '/browse/UWA/'
        After I login into the portal
        Given I access the url "/browse/UWA/"
        Then I see the heading "Participants"

    Scenario: Participants list must be paginated
        After I login into the portal
        Given I access the url "/browse/UWA/"
        Then I see a div for "pagination pagination-centered "

    Scenario: Participant list summary must include a gender 
        After I login into the portal
        Given I access the url "/browse/UWA/"
        Then I see that "participant summary" paragraph 1 is "Gender"

    Scenario: Participant list summary must include a birth year 
        After I login into the portal
        Given I access the url "/browse/UWA/"
        Then I see that "participant summary" paragraph 2 is "Birth Year"

    Scenario: Participant list summary must include a identifier link
        After I login into the portal
        Given I access the url "/browse/UWA/"
        Then I see that "participant summary" paragraph 3 is "Url"

    Scenario: Participants must include a link to browse details 
        After I login into the portal
        Given I access the url "/browse/UWA/"
        Then I see that link 10 is "/browse/UWA/4_488"

    Scenario: Participants list must have a bread crumb link back to sites
        After I login into the portal
        Given I access the url "/browse/UWA/"
        Then I see that link 9 is "/browse/"

    Scenario: Participants must be available when performing faceted browsing
        After I login into the portal
        Given I access the url "/browse/participants/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin"
        Then I see the heading "Participants"