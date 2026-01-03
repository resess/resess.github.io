## UC3: Create Group

This document provides a detailed description of the use case UC3: Create Group. 

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

A user can create a group and become its owner. When creating a group, the group owner provides the group name and specifies their movie genre preferences. The list of genres is fetched from the External Movie Service (TMDB API). 

### Primary Actors

- User  
- External Movie Service (TMDB API)

### Triggers

- User taps the “Create New Group” button on the Group List  screen.

### Success Scenario

1. The system displays a dialog to enter the “Group Name”, with an “Next” button.  
2. User enters a group name and taps the “Next” button.  
3. The system displays the Genre Preferences screen with checkboxes for available genres, which are fetched from the External Movie Service.  
4. User selects checkboxes for each of their preferred movie genres.  
5. User taps the “Create Group” button to create the group and become the group owner.  
6. The system creates the new group and stores its details and the selected genres.   
7. The system calls the [UC5: ‘View Details of a Group’](UC5_View_Details_of_a_Group.md), displaying the Group Details screen. 

### Failure Scenarios

2a. User enters an empty or invalid group name. 

- 2a1. The system displays an error message “Group name is required and must be 3-30 alphanumeric characters.”  
- 2a2. The system continues to present the dialog to enter the group name, which shows the information entered by the user. 

   
3a. The system fails to load the list of genres. 

- 3a1. The system displays an error message “Failed to load movie genres. Please try again.”   
- 3a2. User taps the “Try Again” button.   
- 3a3. The system executes step 3 of the success scenario again. 

5a. User selects no genres. 

- 5a1. The system displays an error message “Genre selection is required. Please choose at least one preferred movie genre.”   
- 5a2. The system continues to present the Genre Preferences screen. 

6a. The system fails to create the group. 

- 6a1. The system displays an error message “Failed to create group. Please try again.”   
- 6a2. User taps the “Try Again” button.  
- 6a3. The system executes step 6 of the success scenario again.
