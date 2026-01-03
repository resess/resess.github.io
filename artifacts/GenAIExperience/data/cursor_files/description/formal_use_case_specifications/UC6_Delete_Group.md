## UC6: Delete Group

This document provides a detailed description of the use case UC6: Delete Group.

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description 

A user can delete groups they own. When a group is deleted, all group members receive a push notification via Push Notification Service (Firebase Cloud Messaging). 

### Primary Actor

- User (group owner)  
- Push Notification Service (Firebase Cloud Messaging)

### Triggers

- User (group owner) taps the “Delete Group” button on the Group Details screen. 

### Success Scenario

1. The system displays a confirmation dialog, asking the user to confirm their decision to permanently delete the group.   
2. User confirms deleting the group by tapping the “Delete” button on the confirmation dialog.   
3. The system deletes the group and its associated details. It presents a confirmation message for deleting the group successfully .  
4. The system uses the Push Notification Service to send a notification to all group members that the group has been deleted. The message format is: “Group {GroupName} has been deleted by the owner.”  
5. The system calls the [UC4: ‘View Groups List’](./UC4_View_Groups_List.md), displaying the Group List screen.

### Failure Scenarios

3a. The system fails to delete the group. 

- 3a1. The system displays an error message “Failed to delete group. Please try again.”   
- 3a2. The system stays on the current screen, displaying the Group Details.

4a. Push Notification Service is unavailable or fails to send notifications. 

- 4a1. The system displays a warning message “You deleted the group successfully but members could not be notified. You might want to contact them directly.”   
- 4a2. The system continues to step 5 of the success scenario. 
