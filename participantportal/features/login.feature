Feature: Authentication within the Participant Portal

    Scenario: Check login window presents login title
        Given I access the url "/participantportal/login/"
        Then I see the heading "Participant Portal"

    Scenario: Check login window presents colour field
        Given I access the url "/participantportal/login/"
        Then I see that label 1 is "Colour"

    Scenario: Check login window presents animal field
        Given I access the url "/participantportal/login/"
        Then I see that label 2 is "Animal"

    Scenario: Check login window presents birth year field
        Given I access the url "/participantportal/login/"
        Then I see that label 3 is "Birth Year"

    Scenario: Check login window presents gender field
        Given I access the url "/participantportal/login/"
        Then I see that label 4 is "Gender"

    Scenario: Check login window presents link to Meta Search Login window
        Given I access the url "/participantportal/login/"
        Then I see that link 1 is "/login/"