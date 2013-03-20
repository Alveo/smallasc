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
        Then I see that "in the search form" paragraph 1 is "Found 3 participant(s)."

    Scenario: Search results includes the appropriate heading
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin&components_field=http%3A%2F%2Fid.austalk.edu.au%2Fcomponent%2F4_540_1_3&participants_field=4_540"
        Then I see the heading "Search Results"

    Scenario: Search results must include a download form
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin&components_field=http%3A%2F%2Fid.austalk.edu.au%2Fcomponent%2F4_540_1_3&participants_field=4_540"
        Then I see the form "Download form"

    Scenario: Search results list items by name
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin&components_field=http%3A%2F%2Fid.austalk.edu.au%2Fcomponent%2F4_540_1_3&participants_field=4_540"
        Then I see that search result 1 is "/browse/ANU/4_540/1/story/4_540_1_3_001"

    Scenario: Search results list items which include a partial prompt
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin&components_field=http%3A%2F%2Fid.austalk.edu.au%2Fcomponent%2F4_540_1_3&participants_field=4_540"
        Then I see the partial prompt "Once upon a time, there was a young rat named Arthur who couldn't make up his mind. Whenever the other ..."

    Scenario: Search results list items should not show the field ID
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin&components_field=http%3A%2F%2Fid.austalk.edu.au%2Fcomponent%2F4_540_1_3&participants_field=4_540"
        Then I should not see the field "ID"

    Scenario: Search results list items should not show the field Audio
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin&components_field=http%3A%2F%2Fid.austalk.edu.au%2Fcomponent%2F4_540_1_3&participants_field=4_540"
        Then I should not see the field "Audio"

    Scenario: Search result list items must be paginated
        After I login into the portal
        Given I access the url "/search/participants/components/?gender=male&ses=Professional&highest_qual=Bachelor+Degree&prof_cat=manager+and+admin&components_field=http%3A%2F%2Fid.austalk.edu.au%2Fcomponent%2F4_540_1_3&participants_field=4_540"
        Then I see a div for "pagination pagination-centered "