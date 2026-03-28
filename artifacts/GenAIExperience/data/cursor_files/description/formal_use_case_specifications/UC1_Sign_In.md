## UC1: Sign In

This document provides a detailed description of use case UC1: Sign In. 

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

To access app features, a user must authenticate using External Authentication Service (Google Authentication Service) first. New users are automatically registered with the app upon the first authentication.

### Primary Actors

- User  
- External Authentication Service (Google Authentication Service)

### Triggers

- User that has not yet signed in or whose authentication token has expired launches the MovieSwipe application.

### Success Scenario

1. The system displays the Authentication screen with the "Sign in with Google" button.  
2. User taps the "Sign in with Google" button.  
3. The system initiates Google authentication flow, prompting the user to provide their Google credentials.  
4. User completes the Google authentication process.  
5. Google Authentication Service authenticates the user.  
6. The system calls the [UC4: ‘View Groups List’](./UC4_View_Groups_List.md), displaying the Group List screen.

### Failure Scenario

3a. Google Authentication Service is unavailable. 

- 3a1. The system displays an error message "Authentication service temporarily unavailable. Please try again."   
- 3a2. The system executes step 1 of the success scenario again.

5a. Authentication fails. 

- 5a1. The system displays an error message "Authentication unsuccessful. Please try again."  
- 5a2. The system executes step 3 of the success scenario again.