## UC4: Delete Account

This document provides a detailed description of the use case UC4: Delete Account.

We describe each use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

An authenticated user can delete their account.

### Primary Actor

- User  
- External Authentication Service (Google Authentication Service)

### Triggers

- User taps the “Delete account” button on the Group List screen.   

### Success Scenario

1. The system initiates the delete account process by calling the Google Authentication Service to end the current session.   
2. Google Authentication Service revokes the user’s authentication token and confirms session termination.   
3. The system deletes the account of the user from the app. 
4. The system presents a confirmation message showing successful account deletion and closes the app.

### Failure Scenarios

1a. Google Authentication Service is unavailable. 

- 1a1. The system displays an error message "Authentication service temporarily unavailable, cannot delete account. Please try again." and stays on its current screen.

3a. The system fails to delete user account. 

- 3a1. The system displays an error message "Account deletion failed. Please try again." and stays on its current screen.
