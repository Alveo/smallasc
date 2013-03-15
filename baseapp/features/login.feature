Feature: Authentication within the BaseApp

    Scenario: Check login window presents username field
        Given I access the url "/login/"
        Then I see that label 1 is "Username"

    Scenario: Check login window presents password field
        Given I access the url "/login/"
        Then I see that label 2 is "Password"

    Scenario: Check login window presents link to ParticipantPortal window
        Given I access the url "/login/"
        Then I see that link 1 is "/participantportal/login/"

    Scenario: Check that an invalid username presents an alert
        Given I access the url "/login/"
        If I set username to "invalidusername" and password to "validpassword" following url "/login/"
        Then I see the alert "Sorry, your username or password wasn't recognized"

    Scenario: Check that an invalid password presents an alert
        Given I access the url "/login/"
        If I set username to "joeblogs" and password to "invalidpassword" following url "/login/"
        Then I see the alert "Sorry, your username or password wasn't recognized"

    Scenario: Check that a valid username and password login takes us to dashboard
        Given I access the url "/login/"
        If I set username to "joeblogs" and password to "password" following url "/login/"
        Then I see the heading "Dashboard"  