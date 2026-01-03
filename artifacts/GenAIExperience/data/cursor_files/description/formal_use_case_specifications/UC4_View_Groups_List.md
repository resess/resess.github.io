## UC4: View Groups List

This document provides a detailed description of the use case UC4: View Groups List

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

## UC4: View Groups List

### Description

A user can view a list of groups they created or joined.

### Primary Actor

- User

### Triggers

- The system redirects User to the Group List screen, either from another screen or when opening the app with the authentication token that has not expired. 

### Success Scenario

1. The system displays the Group List screen, with a list of groups the user has created or joined. Each group item in the list includes the group name and the user’s role: either “owner” or “member”. The screen also contains two buttons: “Create New Group” and “Join Group”.

### Failure Scenarios

1a. The system fails to load the list of groups that the user has created or joined.

- 1a1. The system displays an alert dialog with an error message “Failed to load groups. Please retry.” The dialog has a “Retry” button.  
- 1a2. User taps the “Retry” button.  
- 1a3. The system executes step 1 of the success scenario again, to re-load the groups list.
