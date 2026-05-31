## UC1: Sign Up

This document provides a detailed description of use case UC1: Sign Up. 

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

A new user registers an account using External Authentication Service (Google Authentication Service).

### Primary Actors

- User  
- External Authentication Service (Google Authentication Service)

### Triggers

- User that has not yet signed up.

### Success Scenario

1. The system displays the Authentication screen with the "Sign up with Google" button.  
2. User taps the "Sign up with Google" button.  
3. The system initiates Google authentication flow, prompting the user to provide their Google credentials.  
4. User completes the Google authentication process.  
5. Google Authentication Service authenticates the user.  
6. The system calls the [UC7: ‘View Groups List’](./UC7_View_Groups_List.md), displaying the Group List screen.

### Failure Scenario

3a. Google Authentication Service is unavailable. 

- 3a1. The system displays an error message "Authentication service temporarily unavailable. Please try again."   
- 3a2. The system executes step 1 of the success scenario again.

5a. Authentication fails. 

- 5a1. The system displays an error message "Authentication unsuccessful. Please try again."  
- 5a2. The system executes step 3 of the success scenario again.

5b. User already exists. 

- 5b1. The system displays an error message "The user already exists. Please sign in instead."
- 5b2. The system displays the Authentication screen.