## UC9: Join Group

This document provides a detailed description of the use case UC9: Join Group.

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

A user can join a group using the invitation code shared by the group owner and become a group member. When joining, the user must specify their movie genre preferences. The list of genres is specified for the group by its owner. If a user joins the group while the group is being viewed by the owner, the list of members is automatically updated. 

### Primary Actors

- User

### Triggers

- User taps the "Join Group" button on the Group List screen. 

### Success Scenario

1. The system displays a dialog to enter the “Invitation Code”, with an “Next” button.  
2. User enters an invitation code and taps the “Next” button.  
3. The system displays the Genre Preferences screen with checkboxes for genres specified for the group by its owner.  
4. User selects checkboxes for each of their preferred movie genres.  
5. User taps the "Join" button to join the group and become a group member.  
6. The system adds the user to the group. 
7. The system calls the [UC6: ‘View Details of a Group’](UC6_View_Details_of_a_Group.md), displaying the Group Details screen. 

### Failure Scenarios

2a. User enters invalid invitation code. 

- 2a1. The system displays an error message "Invalid invitation code. Please check the code and try again."  
- 2a2. The system continues to present the dialog to enter the invitation code. 

2b. The group associated with the invitation code has been deleted. 

- 2b1. The system displays an error message "The group has been deleted."   
- 2b2. The system continues to present the Group List screen. 

2c. User is already a member of this group. 

- 2c1. The system displays a message "You are already a member of this group".  
- 2c2. The system calls the [UC6: ‘View Details of a Group’](UC6_View_Details_of_a_Group.md), displaying the Group Details screen.

3a. The system fails to load the list of genres.

- 3a1. The system displays a dialog with an error message "Failed to load movie genres. Please try again." The dialog has a “Retry” button.  
- 3a2. User taps the “Retry” button.  
- 3a3. The system executes step 3 of the success scenario again, to re-load the list of genres.

5a. User selects no genres. 

- 5a1. The system displays an error message "Genre selection is required. Please choose at least one preferred movie genre."   
- 5a2. The system continues to present the Genre Preferences screen. 

6a. The system fails to add the user to the group. 

- 6b1. The system displays an error message "Failed to join group. Please try again."      
- 6b2. The system continues to present the Genre Preferences screen. 
