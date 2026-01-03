## UC5: View Details of a Group

This document provides a detailed description of the use case UC5: View Details of a Group

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

A user can view detailed information of a group where they are the owner or a member. The screen displays different content and actions based on the user's role, the group’s voting session state, and the user's individual voting progress.

### Primary Actor

- User

### Triggers

- User selects a group from the Group List screen, to view the group's detailed information.  
- The system redirects User to the Group Details screen from another app screen.  
- User taps on a notification about the group 

### Success Scenario

1. The system displays the Group Details screen containing two sections: group information and voting information.  
   * Group information section content depends on the user’s role:  
     * If User is the owner of the group: Shows the group name, user’s role (i.e., “owner”), a unique invitation code for member recruitment, list of members in the group, and a “Delete Group” button.  
     * If User is a member of the group: Shows the group name, user’s role (i.e., “member”), and a “Leave Group” button.  
   * Voting information section content depends on the user’s role, the group’s voting session state, and the user’s individual voting progress:  
     * If User is the owner of the group:  
       * If the voting session has not started: Shows a “Start Voting Session” button.  
       * If the voting session has started but not yet ended:  
         1. If User has not voted: Shows a “Join Voting Session” button and an “End Voting Session” button.  
         2. If User has voted for a subset of movies: Shows a “Resume Voting Session” button and an “End Voting Session” button.  
         3. If User has voted for all movies: Shows an “End Voting Session” button.   
       * If the voting session ended: Shows the selected movie (title, poster, genre, rating, length, and summary).   
     * If User is a member of the group:   
       * If the voting session has not started: Shows the text “Waiting for the owner to start the session”.  
       * If the voting session started but not yet ended:  
         1. If User has not voted: Shows a “Join Voting Session” button.  
         2. If User has voted for a subset of movies: Shows a “Resume Voting Session” Button.  
         3. If User has voted for all movies: Shows the text “Waiting for the owner to end the session”.  
       * If the voting session has ended: Shows the selected movie (title, poster, genre, rating, length, and summary).   

### Failure Scenario

1a. The group has been deleted by the owner.

- 1a1. The system displays an error message “This group has been deleted.”  
- 1a2. The system calls the [UC4: ‘View Groups List’](./UC4_View_Groups_List.md), displaying the updated Group List screen.

1b. User is no longer a member of the group. 

- 1b1. The system displays an error message “You are no longer a member of this group.”  
- 1b2. The system calls the [UC4: ‘View Groups List’](./UC4_View_Groups_List.md), displaying the Group List screen with the list of groups for which the user is a member or an owner.

1c. The system fails to load the group and voting information. 

- 1c1. The system displays an error message “Failed to load group information.” and stays on its current screen.
