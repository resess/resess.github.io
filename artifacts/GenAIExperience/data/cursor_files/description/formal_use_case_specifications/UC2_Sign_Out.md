## UC2: Sign Out 

This document provides a detailed description of the use case UC2: Sign Out. 

We describe each use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

An authenticated user can sign out. 

### Primary Actor

- User  
- External Authentication Service (Google Authentication Service)

### Triggers

- User taps the “Sign out” button on the Group List screen.   
- When opening the app, the system redirects User, whose authentication token has expired, to the Authentication screen.

### Success Scenario

1. The system initiates the sign out process by calling the Google Authentication Service to end the current session.   
2. Google Authentication Service revokes the user’s authentication token and confirms session termination.   
3. The system presents a confirmation message showing successful sign out and closes the app.

### Failure Scenarios

1a. Google Authentication Service is unavailable. 

- 1a1. The system displays an error message "Authentication service temporarily unavailable, cannot sign out. Please try again." and stays on its current screen.
